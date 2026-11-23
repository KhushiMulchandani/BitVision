from datetime import datetime, timezone

import pandas as pd
import yfinance as yf
from django.core.management.base import BaseCommand

from core.models import OHLCV

# BTC-USD on Yahoo Finance starts on 2014-09-17: the earliest data that exists.
EARLIEST = "2014-09-17"


class Command(BaseCommand):
    help = "Download BTC-USD daily candles (earliest available date -> yesterday, UTC) into the OHLCV table."

    def handle(self, *args, **options):
        self.stdout.write("Downloading BTC-USD from yfinance...")
        df = yf.download("BTC-USD", start=EARLIEST, interval="1d", progress=False, auto_adjust=True)
        if df.empty:
            self.stderr.write(self.style.ERROR("Failed to fetch data from yfinance."))
            return

        df = df.reset_index()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df["Date"] = pd.to_datetime(df["Date"]).dt.date

        # Today's candle is still forming; training or predicting on it would leak a half-day.
        today_utc = datetime.now(timezone.utc).date()
        df = df[df["Date"] < today_utc].dropna(subset=["Open", "High", "Low", "Close"])

        records = [
            OHLCV(date=r.Date, open=round(float(r.Open), 2), high=round(float(r.High), 2),
                  low=round(float(r.Low), 2), close=round(float(r.Close), 2),
                  volume=int(r.Volume) if pd.notna(r.Volume) else 0)
            for r in df.itertuples(index=False)
        ]
        # Insert new days and refresh existing ones (so corrected candles overwrite old values).
        OHLCV.objects.bulk_create(
            records, batch_size=1000, update_conflicts=True, unique_fields=["date"],
            update_fields=["open", "high", "low", "close", "volume"],
        )
        first = OHLCV.objects.order_by("date").first()
        last = OHLCV.objects.order_by("-date").first()
        self.stdout.write(self.style.SUCCESS(
            f"OHLCV rows: {OHLCV.objects.count()} ({first.date} -> {last.date})"
        ))
