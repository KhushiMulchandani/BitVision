"""Lazy, cached loading of the trained artifacts. Nothing is loaded at Django start-up."""
import json
import joblib
from .paths import (MODELS_DIR, RF_FILE, XGB_FILE, LSTM_FILE, SCALER_FILE, META_FILE, METRICS_FILE)


class ModelsNotTrained(RuntimeError):
    """Raised when an artifact is missing; the message tells the user what to run."""


def _require(name):
    path = MODELS_DIR / name
    if not path.exists():
        raise ModelsNotTrained(f"{path} not found. Train the models first: python manage.py retrain")
    return path


class MLModelLoader:
    _cache = {}

    @classmethod
    def reload(cls):
        cls._cache = {}

    @classmethod
    def _joblib(cls, key, filename):
        if key not in cls._cache:
            cls._cache[key] = joblib.load(_require(filename))
        return cls._cache[key]

    @classmethod
    def get_rf_model(cls):      # {"model", "features"}
        return cls._joblib("rf", RF_FILE)

    @classmethod
    def get_xgb_model(cls):     # {"model", "features"}
        return cls._joblib("xgb", XGB_FILE)

    @classmethod
    def get_scaler(cls):        # {"scaler", "features", "seq_len", "ret_std"}
        return cls._joblib("scaler", SCALER_FILE)

    @classmethod
    def get_meta_model(cls):    # {"model", "sigma", "coverage", "z", ...}
        return cls._joblib("meta", META_FILE)

    @classmethod
    def get_lstm_model(cls):
        if "lstm" not in cls._cache:
            import tensorflow as tf  # imported lazily: TensorFlow is slow to import
            cls._cache["lstm"] = tf.keras.models.load_model(_require(LSTM_FILE))
        return cls._cache["lstm"]

    @classmethod
    def get_metrics(cls):
        with open(_require(METRICS_FILE), encoding="utf-8") as f:
            return json.load(f)
