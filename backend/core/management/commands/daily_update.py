from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Daily job: new candles -> features -> tomorrow's prediction (no retraining)."

    def handle(self, *args, **options):
        call_command("ingest")
        call_command("compute_features")
        call_command("predict_tomorrow")
        call_command("check_alerts")