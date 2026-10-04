import os
import joblib
from django.conf import settings

# Resolves to project root / models directory
MODELS_DIR = getattr(
    settings,
    'MODELS_DIR',
    os.environ.get('MODELS_DIR', str(settings.BASE_DIR.parent / 'models'))
)


class MLModelLoader:
    _lstm_model = None
    _rf_model = None
    _xgb_model = None
    _meta_model = None
    _scaler = None

    @classmethod
    def get_models_dir(cls):
        return MODELS_DIR

    @classmethod
    def get_lstm_model(cls):
        if cls._lstm_model is None:
            # Lazy import TensorFlow so other commands don't pay the startup cost
            import tensorflow as tf
            for candidate in ['lstm_model.keras', 'lstm.h5']:
                path = os.path.join(MODELS_DIR, candidate)
                if os.path.exists(path):
                    cls._lstm_model = tf.keras.models.load_model(path)
                    break
        return cls._lstm_model

    @classmethod
    def get_rf_model(cls):
        if cls._rf_model is None:
            for candidate in ['rf.pkl', 'random_forest_model.pkl', 'rf_model.joblib']:
                path = os.path.join(MODELS_DIR, candidate)
                if os.path.exists(path):
                    cls._rf_model = joblib.load(path)
                    break
        return cls._rf_model

    @classmethod
    def get_xgb_model(cls):
        if cls._xgb_model is None:
            for candidate in ['xgb.pkl', 'xgboost_model.pkl']:
                path = os.path.join(MODELS_DIR, candidate)
                if os.path.exists(path):
                    cls._xgb_model = joblib.load(path)
                    break
        return cls._xgb_model

    @classmethod
    def get_meta_model(cls):
        if cls._meta_model is None:
            for candidate in ['meta.pkl', 'ridge_meta.pkl', 'stacked_ensemble.pkl']:
                path = os.path.join(MODELS_DIR, candidate)
                if os.path.exists(path):
                    cls._meta_model = joblib.load(path)
                    break
        return cls._meta_model

    @classmethod
    def get_scaler(cls):
        if cls._scaler is None:
            for candidate in ['scaler.pkl', 'lstm_scaler.pkl']:
                path = os.path.join(MODELS_DIR, candidate)
                if os.path.exists(path):
                    cls._scaler = joblib.load(path)
                    break
        return cls._scaler