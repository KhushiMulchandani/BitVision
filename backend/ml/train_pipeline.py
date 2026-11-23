"""
BitVision training and evaluation pipeline (spec: RF + XGBoost + LSTM + Ridge meta-learner).

Design (read this before changing anything)
-------------------------------------------
* Every model predicts the NEXT-DAY RETURN, never the price level. Price levels
  are non-stationary (BTC was ~$300 in 2015 and ~$80,000 now), so a model that
  outputs prices cannot extrapolate. Predicted price = close * (1 + predicted return).
* Chronological split 70 % train / 15 % validation / 15 % test. No shuffling.
* Base models are fitted on TRAIN only. Their predictions on the unseen VALIDATION
  block are the out-of-sample inputs the Ridge meta-learner is fitted on; the TEST
  block is used once, for the final numbers.
* The honest yardstick is the naive baseline "tomorrow = today". It is stored
  next to the models so the UI and the report can show whether anything beats it.
* The LSTM target is aligned with its window: the window ends on day t (inclusive)
  and the target is the return from t to t+1.
"""
import json
import os
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

from core.models import ModelMetric, Prediction
from .dataset import load_frame
from .features import (
    SEQ_LEN, TAB_FEATURES, SEQ_FEATURES, Z80,
    split_indices, make_windows, compute_metrics, baseline_metrics, interval_coverage,
)
from .model_loader import MLModelLoader
from .paths import (MODELS_DIR, RF_FILE, XGB_FILE, LSTM_FILE, SCALER_FILE, META_FILE, METRICS_FILE)

SEED = 42


def _build_lstm(n_features):
    import tensorflow as tf
    from tensorflow.keras import layers, models
    model = models.Sequential([
        layers.Input(shape=(SEQ_LEN, n_features)),
        layers.LSTM(64, return_sequences=True),
        layers.Dropout(0.2),
        layers.LSTM(32),
        layers.Dropout(0.2),
        layers.Dense(16, activation="relu"),
        layers.Dense(1),
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss="huber")
    return model


def train_and_evaluate_all(progress_callback=None):
    def log(msg):
        (progress_callback or print)(msg)

    import tensorflow as tf
    tf.keras.utils.set_random_seed(SEED)

    log("Loading data from the database...")
    df = load_frame()                       # last row = today, target unknown
    hist = df.iloc[:-1].reset_index(drop=True)   # rows with a known next-day target
    n = len(hist)
    train_end, val_end = split_indices(n)
    if train_end < SEQ_LEN + 50:
        raise ValueError("Not enough history to train. Run ingest first.")

    log(f"Rows: {n} labelled days, {hist['date'].iloc[0]} -> {hist['date'].iloc[-1]}")
    log(f"Split -> train {train_end}, validation {val_end - train_end}, test {n - val_end}")

    y = hist["target_return"].values
    close = hist["close"].values
    sl_train, sl_val, sl_test = slice(0, train_end), slice(train_end, val_end), slice(val_end, n)

    # ---------------- Random Forest ----------------
    log("Training Random Forest...")
    rf = RandomForestRegressor(n_estimators=300, max_depth=8, min_samples_leaf=10,
                               max_features="sqrt", random_state=SEED, n_jobs=-1)
    rf.fit(hist.iloc[sl_train][TAB_FEATURES], y[sl_train])
    rf_ret = rf.predict(hist[TAB_FEATURES])

    # ---------------- XGBoost ----------------
    log("Training XGBoost...")
    xgb = XGBRegressor(n_estimators=300, max_depth=3, learning_rate=0.03, subsample=0.8,
                       colsample_bytree=0.8, min_child_weight=10, reg_lambda=5.0,
                       random_state=SEED, n_jobs=-1)
    xgb.fit(hist.iloc[sl_train][TAB_FEATURES], y[sl_train])
    xgb_ret = xgb.predict(hist[TAB_FEATURES])

    # ---------------- LSTM (60-day windows) ----------------
    log("Training LSTM...")
    scaler = StandardScaler().fit(df.loc[: train_end - 1, SEQ_FEATURES].values)
    scaled = scaler.transform(df[SEQ_FEATURES].values)
    windows, t_idx = make_windows(scaled, SEQ_LEN)       # windows[k] ends on row t_idx[k]
    ret_std = float(np.std(y[sl_train]))

    labelled = t_idx < n                                  # windows whose target is known
    X_lab, t_lab = windows[labelled], t_idx[labelled]
    y_lab = y[t_lab] / ret_std                            # aligned: window ends t, target t -> t+1
    train_mask = t_lab < train_end

    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    lstm = _build_lstm(len(SEQ_FEATURES))
    lstm.fit(
        X_lab[train_mask], y_lab[train_mask],
        epochs=40, batch_size=64, validation_split=0.1, verbose=0,
        callbacks=[EarlyStopping(monitor="val_loss", patience=6, restore_best_weights=True),
                   ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, min_lr=1e-5)],
    )
    lstm_ret = np.full(n, np.nan)
    lstm_ret[t_lab] = lstm.predict(X_lab, verbose=0).flatten() * ret_std
    if np.isnan(lstm_ret[train_end:]).any():
        raise RuntimeError("LSTM predictions missing for validation/test rows")

    # ---------------- Stacked ensemble (Ridge meta-learner) ----------------
    log("Fitting the Ridge meta-learner on validation-block predictions...")
    base = np.column_stack([rf_ret, xgb_ret, lstm_ret])
    # returns are tiny numbers, so work in percent to make the Ridge penalty meaningful
    meta = Ridge(alpha=1.0, positive=True)
    meta.fit(base[sl_val] * 100.0, y[sl_val] * 100.0)
    stacked_ret = np.full(n, np.nan)
    stacked_ret[train_end:] = meta.predict(base[train_end:] * 100.0) / 100.0
    log(f"Meta-learner weights -> RF {meta.coef_[0]:.3f}, XGB {meta.coef_[1]:.3f}, LSTM {meta.coef_[2]:.3f}")

    preds = {"rf": rf_ret, "xgb": xgb_ret, "lstm": lstm_ret, "stacked": stacked_ret}

    # Uncertainty: std of validation residuals -> 80 % interval. Confidence stored for a model is
    # the share of TEST days that really fell inside that interval (empirical coverage).
    sigma = {c: float(np.std(y[sl_val] - preds[c][sl_val])) for c in preds}
    coverage = {c: round(interval_coverage(y[sl_test], preds[c][sl_test], sigma[c]), 3) for c in preds}

    # ---------------- Evaluation on the TEST block (price scale) ----------------
    y_price = close[sl_test] * (1.0 + y[sl_test])
    metrics = {c: compute_metrics(y_price, close[sl_test] * (1.0 + preds[c][sl_test]), close[sl_test])
               for c in preds}
    metrics["baseline"] = baseline_metrics(y_price, close[sl_test])
    for c, m in metrics.items():
        log(f"{c:9s} RMSE {m['rmse']:>9} | MAE {m['mae']:>9} | MAPE {m['mape']:>6}% | DirAcc {m['directional_accuracy']}%")

    best_single = min(["rf", "xgb", "lstm"], key=lambda c: metrics[c]["rmse"])
    verdict = {
        "best_single_model": best_single,
        "stacked_beats_best_single": metrics["stacked"]["rmse"] < metrics[best_single]["rmse"],
        "models_beating_baseline_rmse": [c for c in preds if metrics[c]["rmse"] < metrics["baseline"]["rmse"]],
    }
    log(f"Models beating the naive baseline on RMSE: {verdict['models_beating_baseline_rmse'] or 'none'}")

    # ---------------- Save artifacts ----------------
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": rf, "features": TAB_FEATURES}, MODELS_DIR / RF_FILE)
    joblib.dump({"model": xgb, "features": TAB_FEATURES}, MODELS_DIR / XGB_FILE)
    lstm.save(MODELS_DIR / LSTM_FILE)
    joblib.dump({"scaler": scaler, "features": SEQ_FEATURES, "seq_len": SEQ_LEN, "ret_std": ret_std},
                MODELS_DIR / SCALER_FILE)
    joblib.dump({"model": meta, "base_models": ["rf", "xgb", "lstm"], "sigma": sigma,
                 "coverage": coverage, "z": Z80, "trained_through": str(hist["date"].iloc[-1])},
                MODELS_DIR / META_FILE)
    report = {
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_start": str(hist["date"].iloc[0]), "data_end": str(hist["date"].iloc[-1]),
        "rows": {"train": train_end, "validation": val_end - train_end, "test": n - val_end},
        "test_period": [str(hist["date"].iloc[val_end]), str(hist["date"].iloc[-1])],
        "meta_weights": dict(zip(["rf", "xgb", "lstm"], [round(float(w), 4) for w in meta.coef_])),
        "metrics": metrics, "interval_coverage_80": coverage, "verdict": verdict,
    }
    with open(MODELS_DIR / METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    MLModelLoader.reload()

    # ---------------- Database: metrics + backtest predictions ----------------
    log("Writing ModelMetric and backtest Prediction rows...")
    ModelMetric.objects.all().delete()           # only the latest run is kept (history: metrics.json)
    ModelMetric.objects.bulk_create([
        ModelMetric(model_name=c, rmse=m["rmse"], mae=m["mae"], mape=m["mape"],
                    directional_accuracy=m["directional_accuracy"])
        for c, m in metrics.items()
    ])

    # Prediction.date is the day BEING PREDICTED (the day after the input row).
    Prediction.objects.filter(model_used__in=list(preds)).delete()
    rows = []
    for i in range(val_end, n):
        target_date = (pd.to_datetime(hist["date"].iloc[i]) + pd.Timedelta(days=1)).date()
        actual = round(float(close[i] * (1.0 + y[i])), 2)
        for c in preds:
            price = close[i] * (1.0 + preds[c][i])
            lo = close[i] * (1.0 + preds[c][i] - Z80 * sigma[c])
            hi = close[i] * (1.0 + preds[c][i] + Z80 * sigma[c])
            rows.append(Prediction(date=target_date, model_used=c, predicted_price=round(float(price), 2),
                                   actual_price=actual, confidence=coverage[c],
                                   lower_price=round(float(lo), 2), upper_price=round(float(hi), 2)))
    Prediction.objects.bulk_create(rows, batch_size=1000)
    log("Training finished. Next: python manage.py predict_tomorrow")
    return report
