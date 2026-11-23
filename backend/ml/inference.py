"""
Live prediction for the next day, using the saved artifacts and the same
feature code as training. The ONLY inference path in the project: used by
`manage.py predict_tomorrow` and (later) by /api/predict/.
"""
import numpy as np
import pandas as pd

from .dataset import load_frame
from .features import SEQ_LEN, interval_from_return
from .model_loader import MLModelLoader


def predict_latest() -> dict:
    df = load_frame()
    latest = df.iloc[-1]
    close = float(latest["close"])
    based_on = pd.to_datetime(latest["date"])
    target_date = (based_on + pd.Timedelta(days=1)).date()

    rf = MLModelLoader.get_rf_model()
    xgb = MLModelLoader.get_xgb_model()
    sc = MLModelLoader.get_scaler()
    meta = MLModelLoader.get_meta_model()
    lstm = MLModelLoader.get_lstm_model()

    x_tab = pd.DataFrame([latest[rf["features"]].astype(float).to_dict()])
    r_rf = float(rf["model"].predict(x_tab)[0])
    r_xgb = float(xgb["model"].predict(x_tab[xgb["features"]])[0])

    window = df[sc["features"]].values[-sc["seq_len"]:].astype(np.float32)
    if len(window) < sc["seq_len"]:
        raise ValueError("Not enough history for the LSTM window")
    window = sc["scaler"].transform(window).reshape(1, sc["seq_len"], len(sc["features"]))
    r_lstm = float(lstm.predict(window, verbose=0).flatten()[0]) * sc["ret_std"]

    r_stacked = float(meta["model"].predict(np.array([[r_rf, r_xgb, r_lstm]]) * 100.0)[0]) / 100.0

    out = {}
    for code, r in [("rf", r_rf), ("xgb", r_xgb), ("lstm", r_lstm), ("stacked", r_stacked)]:
        price, lo, hi = interval_from_return(close, r, meta["sigma"][code], meta["z"])
        out[code] = {
            "predicted_return": r,
            "predicted_price": price,
            "lower_price": lo,
            "upper_price": hi,
            "confidence": meta["coverage"][code],   # share of test days inside the interval
        }
    return {
        "based_on_date": str(based_on.date()),
        "date": str(target_date),               # the day being predicted
        "current_close": close,
        "direction": "up" if r_stacked > 0 else "down",
        "models": out,
    }
