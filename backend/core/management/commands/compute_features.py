import pandas as pd
from django.core.management.base import BaseCommand
from core.models import OHLCV, Feature


class Command(BaseCommand):
    help = "Calculates technical indicators and lag features from OHLCV data and stores them in the Feature model."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Fetching OHLCV data from database..."))

        # 1. Fetch OHLCV data and convert to DataFrame
        qs = OHLCV.objects.all().order_by("date").values("date", "close", "high", "low", "volume")
        if not qs.exists():
            self.stdout.write(self.style.ERROR("No OHLCV data found! Run 'python manage.py ingest' first."))
            return

        df = pd.DataFrame(list(qs))
        df.set_index("date", inplace=True)

        self.stdout.write(self.style.NOTICE(f"Calculating technical indicators for {len(df)} records..."))

        # 2. Moving Averages (ma_20, ma_50)
        df["ma_20"] = df["close"].rolling(window=20).mean()
        df["ma_50"] = df["close"].rolling(window=50).mean()

        # 3. RSI (14-day)
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi_14"] = 100 - (100 / (1 + rs))

        # 4. MACD (12-period EMA - 26-period EMA) & Signal Line
        ema_12 = df["close"].ewm(span=12, adjust=False).mean()
        ema_26 = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = ema_12 - ema_26
        df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

        # 5. Bollinger Bands (20-day SMA +/- 2 Std Dev)
        rolling_std = df["close"].rolling(window=20).std()
        df["bollinger_upper"] = df["ma_20"] + (rolling_std * 2)
        df["bollinger_lower"] = df["ma_20"] - (rolling_std * 2)

        # 6. Lag Features
        df["lag_1"] = df["close"].shift(1)
        df["lag_7"] = df["close"].shift(7)

        # 7. Bulk Save to Feature Model
        self.stdout.write(self.style.NOTICE("Saving calculated features into database..."))

        feature_objects = []
        for date, row in df.iterrows():
            feature_objects.append(
                Feature(
                    date=date,
                    rsi_14=row["rsi_14"] if pd.notna(row["rsi_14"]) else None,
                    macd=row["macd"] if pd.notna(row["macd"]) else None,
                    macd_signal=row["macd_signal"] if pd.notna(row["macd_signal"]) else None,
                    ma_20=row["ma_20"] if pd.notna(row["ma_20"]) else None,
                    ma_50=row["ma_50"] if pd.notna(row["ma_50"]) else None,
                    bollinger_upper=row["bollinger_upper"] if pd.notna(row["bollinger_upper"]) else None,
                    bollinger_lower=row["bollinger_lower"] if pd.notna(row["bollinger_lower"]) else None,
                    fg_index=None,  # External Fear & Greed index can be updated separately
                    lag_1=row["lag_1"] if pd.notna(row["lag_1"]) else None,
                    lag_7=row["lag_7"] if pd.notna(row["lag_7"]) else None,
                )
            )

        # Delete old computed features & bulk insert new ones
        Feature.objects.all().delete()
        Feature.objects.bulk_create(feature_objects, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f"Successfully computed and stored features for {len(feature_objects)} records!"))