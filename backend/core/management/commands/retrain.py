from django.core.management import call_command
from django.core.management.base import BaseCommand

from ml.train_pipeline import train_and_evaluate_all


class Command(BaseCommand):
    help = "Refresh data and features, retrain RF / XGBoost / LSTM / stacked model, then predict tomorrow."

    def add_arguments(self, parser):
        parser.add_argument("--skip-ingest", action="store_true", help="Use the data already in the database.")

    def handle(self, *args, **options):
        if not options["skip_ingest"]:
            call_command("ingest")
        call_command("compute_features")
        report = train_and_evaluate_all(progress_callback=self.stdout.write)
        v = report["verdict"]
        self.stdout.write(self.style.SUCCESS(
            f"Trained on {report['data_start']} -> {report['data_end']}. "
            f"Best single model: {v['best_single_model']}. Stacked beats it: {v['stacked_beats_best_single']}."
        ))
        call_command("predict_tomorrow")
