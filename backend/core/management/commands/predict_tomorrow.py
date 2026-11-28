from django.core.management.base import BaseCommand

from core.models import OHLCV, Prediction
from ml.inference import predict_latest
from core.services import save_prediction_result


class Command(BaseCommand):
    help = "Predict the next day with all models, store the rows, and fill in actual prices of past predictions."

    def handle(self, *args, **options):
        # 1. Back-fill actual prices for earlier predictions whose day has now closed
        filled = 0
        closes = {o.date: o.close for o in OHLCV.objects.order_by("-date")[:60]}
        for p in Prediction.objects.filter(actual_price__isnull=True, date__in=list(closes)):
            p.actual_price = closes[p.date]
            p.save(update_fields=["actual_price"])
            filled += 1
        if filled:
            self.stdout.write(f"Filled actual price for {filled} earlier predictions.")

        # 2. Predict the next day
        result = predict_latest()
        save_prediction_result(result)
        s = result["models"]["stacked"]
        self.stdout.write(self.style.SUCCESS(
            f"{result['date']}: ${s['predicted_price']:,.2f} ({result['direction']}) "
            f"range ${s['lower_price']:,.2f} - ${s['upper_price']:,.2f}  [based on close of {result['based_on_date']}: ${result['current_close']:,.2f}]"
        ))
        for code in ("rf", "xgb", "lstm"):
            self.stdout.write(f"  {code:5s} ${result['models'][code]['predicted_price']:,.2f}")
