from django.core.management.base import BaseCommand

from core.alerts import check_alerts


class Command(BaseCommand):
    help = "Mark price alerts as triggered when the latest close has crossed their target."

    def handle(self, *args, **options):
        n = check_alerts()
        self.stdout.write(self.style.SUCCESS(f"Alerts triggered: {n}"))