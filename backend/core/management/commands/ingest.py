import pandas as pd
import yfinance as yf
from django.core.management.base import BaseCommand
from core.models import OHLCV


class Command(BaseCommand):
    help = "Fetch historical Bitcoin data from yfinance and populate the OHLCV database table"

    def handle(self, *args, **options):
        self.stdout.write("Downloading Bitcoin raw data from yfinance...")
        
        # 1. Download raw BTC data
        df = yf.download('BTC-USD', start='2015-01-01', progress=False)
        
        if df.empty:
            self.stderr.write(self.style.ERROR("Failed to fetch data from yfinance."))
            return

        # 2. Reset index and flatten multi-level column names
        df = df.reset_index()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Ensure correct string format for dates (YYYY-MM-DD)
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

        self.stdout.write(f"Processing {len(df)} records into Django database...")

        # 3. Create model instances
        records = [
            OHLCV(
                date=row['Date'],
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume']),
            )
            for _, row in df.iterrows()
        ]

        # 4. Save to DB without duplicate errors
        OHLCV.objects.bulk_create(records, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully ingested data! Total rows in OHLCV table: {OHLCV.objects.count()}"
            )
        )