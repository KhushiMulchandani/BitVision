"""Load OHLCV + Feature rows from the database as one model-ready DataFrame."""
import pandas as pd
from core.models import OHLCV, Feature
from .features import build_frame


def load_frame() -> pd.DataFrame:
    ohlcv = pd.DataFrame(list(OHLCV.objects.order_by("date").values("date", "open", "high", "low", "close", "volume")))
    feat = pd.DataFrame(list(Feature.objects.order_by("date").values()))
    if ohlcv.empty or feat.empty:
        raise ValueError("OHLCV and Feature tables must be populated first (ingest, compute_features).")
    feat = feat.drop(columns=["id"], errors="ignore")
    return build_frame(ohlcv, feat)
