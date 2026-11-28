import logging
from datetime import timedelta

from ml.inference import predict_latest
from ml.model_loader import MLModelLoader, ModelsNotTrained
from .models import OHLCV, Prediction
from django.utils import timezone

logger = logging.getLogger(__name__)

MODEL_CODES = ("rf", "xgb", "lstm", "stacked")
MODEL_LABELS = {
    "rf": "Random Forest", "xgb": "XGBoost", "lstm": "LSTM",
    "stacked": "Stacked Ensemble (Ridge)", "baseline": "Naive (tomorrow = today)",
}

def _today():
    return timezone.now().date()
class PredictionUnavailable(Exception):
    pass


def save_prediction_result(result):
    """Store the output of ml.inference.predict_latest() as Prediction rows."""
    for code, m in result["models"].items():
        Prediction.objects.update_or_create(
            date=result["date"], model_used=code,
            defaults={
                "predicted_price": round(m["predicted_price"], 2),
                "actual_price": None,
                "confidence": m["confidence"],
                "lower_price": round(m["lower_price"], 2),
                "upper_price": round(m["upper_price"], 2),
            },
        )


def _rows_for(day):
    return {p.model_used: p for p in Prediction.objects.filter(date=day, model_used__in=MODEL_CODES)}


def _entry(p):
    return {
        "label": MODEL_LABELS[p.model_used],
        "predicted_price": float(p.predicted_price),
        "lower_price": float(p.lower_price) if p.lower_price is not None else None,
        "upper_price": float(p.upper_price) if p.upper_price is not None else None,
        "confidence": p.confidence,        # share of test days that fell inside the range
    }


def get_prediction_payload():
    latest = OHLCV.objects.order_by("-date").first()
    if latest is None:
        raise PredictionUnavailable("No price data. Run: python manage.py ingest")

    expected = latest.date + timedelta(days=1)
    rows = _rows_for(expected)

    if "stacked" not in rows:                       # nothing stored for tomorrow -> live inference once
        try:
            save_prediction_result(predict_latest())
            rows = _rows_for(expected)
        except Exception:
            logger.exception("Live inference failed")

    stale = False
    if "stacked" not in rows:                       # fall back to the newest stored prediction
        newest = Prediction.objects.filter(model_used="stacked").order_by("-date").first()
        if newest is None:
            raise PredictionUnavailable("No predictions yet. Run: python manage.py predict_tomorrow")
        rows = _rows_for(newest.date)
        stale = True

    pred_date = rows["stacked"].date
    stale = stale or pred_date < _today()
    base = OHLCV.objects.filter(date=pred_date - timedelta(days=1)).first() or latest
    close = float(base.close)
    stacked = _entry(rows["stacked"])

    try:
        weights = MLModelLoader.get_metrics().get("meta_weights")
    except (ModelsNotTrained, OSError, ValueError):
        weights = None

    return {
        "currency": "USD",
        "date": str(pred_date),
        "based_on_date": str(base.date),
        "current_close": close,
        "direction": "up" if stacked["predicted_price"] > close else "down",
        "stale": stale,
        "predicted_price": stacked["predicted_price"],
        "lower_price": stacked["lower_price"],
        "upper_price": stacked["upper_price"],
        "confidence": stacked["confidence"],
        "models": {code: _entry(p) for code, p in rows.items()},
        "baseline": {"label": MODEL_LABELS["baseline"], "predicted_price": close,
                     "note": "Reference only: assumes no change. No range, no skill claimed."},
        "ensemble_weights": weights,
    }