"""
Pure feature / window / metric helpers for the BitVision ML pipeline.

No Django, TensorFlow or database imports here, so this file can be unit-tested
and re-used by training (train_pipeline.py) and live inference (inference.py).
Training and inference MUST use these same functions, otherwise the model sees
different inputs in production than it saw in training.

Conventions
-----------
* Row t is "today". target_return[t] = close[t+1] / close[t] - 1  (next-day return).
* A window for row t holds the SEQ_LEN rows t-SEQ_LEN+1 ... t (today included).
* All model inputs are stationary (returns, ratios, bounded indicators) so the
  models are not asked to extrapolate to price levels they have never seen.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

SEQ_LEN = 60
Z80 = 1.2816  # z-score for an 80% prediction interval

# Tabular inputs for Random Forest / XGBoost (the spec's DB features, made stationary)
TAB_FEATURES = [
    "rsi_14", "macd_pct", "macd_signal_pct",
    "norm_ma20", "norm_ma50", "norm_boll_u", "norm_boll_l",
    "fg_norm", "norm_lag1", "norm_lag7",
]

# Per-day inputs for the LSTM (60-day window of these)
SEQ_FEATURES = ["daily_return", "hl_range", "vol_chg", "norm_ma20", "rsi_14"]

MODEL_CODES = ["rf", "xgb", "lstm", "stacked"]

_FLOAT_COLS = [
    "open", "high", "low", "close", "volume",
    "rsi_14", "macd", "macd_signal", "ma_20", "ma_50",
    "bollinger_upper", "bollinger_lower", "fg_index", "lag_1", "lag_7",
]


def build_frame(ohlcv: pd.DataFrame, feat: pd.DataFrame) -> pd.DataFrame:
    """
    Join OHLCV with the stored indicators and derive stationary model inputs.

    Returns one row per day, oldest first, starting at the first day where every
    input exists. The LAST row is "today": its target_return is NaN because
    tomorrow's close is not known yet.
    """
    df = ohlcv.merge(feat, on="date", how="inner").sort_values("date").reset_index(drop=True)
    for col in _FLOAT_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce") if col in df.columns else np.nan

    close = df["close"]
    df["daily_return"] = close.pct_change()
    df["hl_range"] = (df["high"] - df["low"]) / close
    vol = df["volume"].where(df["volume"] > 0)
    df["vol_chg"] = np.log(vol / vol.shift(1)).clip(-3, 3).fillna(0.0)

    df["norm_ma20"] = (close - df["ma_20"]) / df["ma_20"]
    df["norm_ma50"] = (close - df["ma_50"]) / df["ma_50"]
    df["norm_boll_u"] = (df["bollinger_upper"] - close) / close
    df["norm_boll_l"] = (close - df["bollinger_lower"]) / close
    df["norm_lag1"] = (close - df["lag_1"]) / df["lag_1"]
    df["norm_lag7"] = (close - df["lag_7"]) / df["lag_7"]
    df["macd_pct"] = df["macd"] / close
    df["macd_signal_pct"] = df["macd_signal"] / close

    # Fear & Greed starts in Feb 2018. Earlier days (and any gaps) are treated as
    # neutral (50) so we can still train on the full price history.
    df["fg_index"] = df["fg_index"].ffill().fillna(50.0)
    df["fg_norm"] = (df["fg_index"] - 50.0) / 50.0

    df["target_return"] = close.shift(-1) / close - 1.0

    required = TAB_FEATURES + SEQ_FEATURES
    ok = df[required].notna().all(axis=1)
    if not ok.any():
        raise ValueError("No rows with complete features. Run ingest and compute_features first.")
    df = df.iloc[int(ok.values.argmax()):].reset_index(drop=True)
    if df[required].isna().any().any():
        raise ValueError("Unexpected gaps in the feature table after the warm-up period.")
    return df


def split_indices(n_hist: int):
    """Chronological 70 / 15 / 15 split boundaries for n_hist labelled rows."""
    train_end = int(n_hist * 0.70)
    val_end = int(n_hist * 0.85)
    return train_end, val_end


def make_windows(values: np.ndarray, seq_len: int = SEQ_LEN):
    """
    Sliding windows. windows[k] = values[k : k+seq_len], which ends at row
    t = k + seq_len - 1 ("today" for that window). Returns (windows, t_index).
    """
    values = np.asarray(values, dtype=np.float32)
    n = len(values)
    if n < seq_len:
        raise ValueError("Not enough rows for one window")
    idx = np.arange(seq_len - 1, n)
    windows = np.stack([values[t - seq_len + 1: t + 1] for t in idx])
    return windows, idx


def compute_metrics(y_true_price, y_pred_price, current_close):
    """RMSE, MAE, MAPE (%) and directional accuracy (%) on the PRICE scale."""
    y_true = np.asarray(y_true_price, dtype=float)
    y_pred = np.asarray(y_pred_price, dtype=float)
    cur = np.asarray(current_close, dtype=float)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    mape = float(np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1e-8))) * 100)
    dir_acc = float(np.mean((y_true > cur) == (y_pred > cur)) * 100)
    return {
        "rmse": round(rmse, 2),
        "mae": round(mae, 2),
        "mape": round(mape, 3),
        "directional_accuracy": round(dir_acc, 2),
    }


def baseline_metrics(y_true_price, current_close):
    """
    Naive 'tomorrow = today' baseline. It never predicts a direction, so its
    directional accuracy is reported as the share of up-days, i.e. what an
    'always up' rule would score. Any real model should beat both numbers.
    """
    m = compute_metrics(y_true_price, current_close, current_close)
    y_true = np.asarray(y_true_price, dtype=float)
    cur = np.asarray(current_close, dtype=float)
    m["directional_accuracy"] = round(float(np.mean(y_true > cur) * 100), 2)
    return m


def interval_from_return(close: float, pred_return: float, sigma: float, z: float = Z80):
    """Price prediction and its interval: close * (1 + r +/- z*sigma)."""
    price = close * (1.0 + pred_return)
    lower = close * (1.0 + pred_return - z * sigma)
    upper = close * (1.0 + pred_return + z * sigma)
    return price, lower, upper


def interval_coverage(true_return, pred_return, sigma: float, z: float = Z80) -> float:
    """Share of days the true return fell inside pred +/- z*sigma."""
    err = np.abs(np.asarray(true_return) - np.asarray(pred_return))
    return float(np.mean(err <= z * sigma))
