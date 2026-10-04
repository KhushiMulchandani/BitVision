import datetime
from decimal import Decimal
import pandas as pd
import yfinance as yf
from django.core.management.base import BaseCommand
from core.models import OHLCV


class Command(BaseCommand):
    help = "Fetch historical Bitcoin data from yfinance and populate the OHLCV database table"

    def add_arguments(self, parser):
        parser.add_argument(
            '--full',
            action='store_true',
            help='Perform a full re-download from 2015 rather than incremental update',
        )
        parser.add_argument(
            '--start',
            type=str,
            default=None,
            help='Start date in YYYY-MM-DD format (overrides automatic calculation)',
        )

    def handle(self, *args, **options):
        is_full = options.get('full', False)
        custom_start = options.get('start')

        latest_record = OHLCV.objects.order_by('-date').first()

        if custom_start:
            start_date = custom_start
        elif is_full or not latest_record:
            start_date = '2015-01-01'
        else:
            # Overlap by 5 days to capture any candle adjustments or revisions
            overlap_date = latest_record.date - datetime.timedelta(days=5)
            start_date = overlap_date.strftime('%Y-%m-%d')

        self.stdout.write(f"Downloading Bitcoin daily OHLCV from yfinance starting {start_date}...")

        try:
            df = yf.download('BTC-USD', start=start_date, progress=False)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to fetch data from yfinance: {e}"))
            return

        if df.empty:
            self.stdout.write(self.style.WARNING("No new data returned by yfinance."))
            return

        # Flatten multi-level columns if present
        df = df.reset_index()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

        records_to_create = []
        records_to_update = []

        existing_dates = set(
            OHLCV.objects.filter(date__gte=df['Date'].min()).values_list('date', flat=True)
        )
        # Convert existing_dates elements to string format for comparison
        existing_date_strs = {d.strftime('%Y-%m-%d') if hasattr(d, 'strftime') else str(d) for d in existing_dates}

        for _, row in df.iterrows():
            d_str = row['Date']
            try:
                open_val = Decimal(f"{float(row['Open']):.2f}")
                high_val = Decimal(f"{float(row['High']):.2f}")
                low_val = Decimal(f"{float(row['Low']):.2f}")
                close_val = Decimal(f"{float(row['Close']):.2f}")
                vol_val = int(round(float(row['Volume']))) if pd.notna(row['Volume']) else 0
            except (ValueError, TypeError):
                continue

            ohlcv_obj = OHLCV(
                date=d_str,
                open=open_val,
                high=high_val,
                low=low_val,
                close=close_val,
                volume=vol_val,
            )

            if d_str in existing_date_strs:
                records_to_update.append(ohlcv_obj)
            else:
                records_to_create.append(ohlcv_obj)

        if records_to_create:
            OHLCV.objects.bulk_create(records_to_create, ignore_conflicts=True)
        if records_to_update:
            # Update overlapping recent records to keep prices fresh
            for obj in records_to_update:
                OHLCV.objects.filter(date=obj.date).update(
                    open=obj.open,
                    high=obj.high,
                    low=obj.low,
                    close=obj.close,
                    volume=obj.volume,
                )

        total_count = OHLCV.objects.count()
        latest = OHLCV.objects.order_by('-date').first()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully ingested data! Created: {len(records_to_create)}, Updated: {len(records_to_update)}. "
                f"Total OHLCV rows: {total_count}. Latest date: {latest.date if latest else 'N/A'}"
            )
        )