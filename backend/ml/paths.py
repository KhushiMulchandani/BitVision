"""Where trained artifacts live: <repo>/models (override with MODEL_DIR in .env)."""
import os
from pathlib import Path
from django.conf import settings

MODELS_DIR = Path(os.environ.get("MODEL_DIR") or Path(settings.BASE_DIR).parent / "models")

RF_FILE = "rf.pkl"
XGB_FILE = "xgb.pkl"
LSTM_FILE = "lstm_model.keras"
SCALER_FILE = "lstm_scaler.pkl"
META_FILE = "meta.pkl"
METRICS_FILE = "metrics.json"
