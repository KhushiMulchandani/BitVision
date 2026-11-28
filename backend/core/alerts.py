from django.db.models import Q
from django.utils import timezone

from .models import Alert, OHLCV


def check_alerts():
    """Trigger every pending alert the latest daily close has crossed. Returns how many fired."""
    latest = OHLCV.objects.order_by("-date").first()
    if latest is None:
        return 0
    price = latest.close
    crossed = Alert.objects.filter(is_triggered=False).filter(
        Q(direction="above", target_price__lte=price) | Q(direction="below", target_price__gte=price)
    )
    return crossed.update(is_triggered=True, triggered_at=timezone.now())