import os
import tensorflow as tf
import joblib
from django.conf import settings

# Adjust the path to point correctly to your trained models directory
MODELS_DIR = os.path.join(settings.BASE_DIR, '..', 'BitVision', 'models')

class MLModelLoader:
    _lstm_model = None
    _rf_model = None

    @classmethod
    def get_lstm_model(cls):
        if cls._lstm_model is None:
            keras_path = os.path.join(MODELS_DIR, 'lstm_model.keras')
            cls._lstm_model = tf.keras.models.load_model(keras_path)
        return cls._lstm_model

    @classmethod
    def get_rf_model(cls):
        if cls._rf_model is None:
            rf_path = os.path.join(MODELS_DIR, 'rf_model.joblib')
            if os.path.exists(rf_path):
                cls._rf_model = joblib.load(rf_path)
        return cls._rf_model