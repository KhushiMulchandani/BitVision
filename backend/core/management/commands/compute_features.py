import datetime
import requests
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import OHLCV, Feature


def compute_rsi(series, period=14):
    """Computes Wilder's smoothed RSI (standard formula)."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    
    # Wilder's exponential smoothing: alpha = 1 / period
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False).mean()
    
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50.0)


def fetch_fear_and_greed_series():
    """
    Fetches the complete historical Fear & Greed Index from Alternative.me.
    Returns a pandas Series indexed by date string 'YYYY-MM-DD'.
    """
    url = "https://api.alternative.me/fng/?limit=0"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            items = resp.json().get("data", [])
            fng_dict = {}
            for item in items:
                ts = int(item["timestamp"])
                d_str = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
                fng_dict[d_str] = float(item["value"])
            return pd.Series(fng_dict, name="fg_index")
    except Exception as e:
        print(f"Warning: Could not fetch Fear & Greed data from alternative.me ({e}). Using neutral values.")
    return pd.Series(dtype=float, name="fg_index")


class Command(BaseCommand):
    help = "Calculates technical indicators, fetches Fear & Greed sentiment, and populates the Feature model."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Fetching OHLCV records from database..."))

        qs = OHLCV.objects.all().order_by("date").values("date", "close", "high", "low", "volume")
        if not qs.exists():
            self.stdout.write(self.style.ERROR("No OHLCV data found! Run 'python manage.py ingest' first."))
            return

        df = pd.DataFrame(list(qs))
        # Ensure date is string format YYYY-MM-DD
        df["date"] = df["date"].astype(str)
        df.set_index("date", inplace=True)
        df["close"] = df["close"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["volume"] = df["volume"].astype(float)

        self.stdout.write(self.style.NOTICE(f"Calculating technical indicators for {len(df)} records..."))

        # 1. Moving Averages (ma_20, ma_50)
        df["ma_20"] = df["close"].rolling(window=20).mean()
        df["ma_50"] = df["close"].rolling(window=50).mean()

        # 2. RSI (14-day Wilder's smoothed)
        df["rsi_14"] = compute_rsi(df["close"], period=14)

        # 3. MACD (12 EMA - 26 EMA) & Signal Line (9 EMA of MACD)
        ema_12 = df["close"].ewm(span=12, adjust=False).mean()
        ema_26 = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = ema_12 - ema_26
        df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()

        # 4. Bollinger Bands (20-day SMA +/- 2 Std Dev)
        rolling_std = df["close"].rolling(window=20).std()
        df["bollinger_upper"] = df["ma_20"] + (rolling_std * 2)
        df["bollinger_lower"] = df["ma_20"] - (rolling_std * 2)

        # 5. Lag Features
        df["lag_1"] = df["close"].shift(1)
        df["lag_7"] = df["close"].shift(7)

        # 6. Fetch and merge Fear & Greed Index
        self.stdout.write(self.style.NOTICE("Fetching Fear & Greed sentiment index..."))
        fng_series = fetch_fear_and_greed_series()

        if not fng_series.empty:
            df = df.join(fng_series, how="left")
            # Forward-fill and backfill gaps, fill dates before index inception (pre-Feb 2018) with 50.0 (Neutral)
            df["fg_index"] = df["fg_index"].ffill().bfill().fillna(50.0)
            self.stdout.write(self.style.SUCCESS(f"Merged {fng_series.count()} Fear & Greed data points!"))
        else:
            df["fg_index"] = 50.0

        # 7. Bulk Save to Feature Model
        self.stdout.write(self.style.NOTICE("Saving calculated features into database..."))

        feature_objects = []
        for date_str, row in df.iterrows():
            feature_objects.append(
                Feature(
                    date=date_str,
                    rsi_14=round(float(row["rsi_14"]), 4) if pd.notna(row["rsi_14"]) else None,
                    macd=round(float(row["macd"]), 4) if pd.notna(row["macd"]) else None,
                    macd_signal=round(float(row["macd_signal"]), 4) if pd.notna(row["macd_signal"]) else None,
                    ma_20=round(float(row["ma_20"]), 2) if pd.notna(row["ma_20"]) else None,
                    ma_50=round(float(row["ma_50"]), 2) if pd.notna(row["ma_50"]) else None,
                    bollinger_upper=round(float(row["bollinger_upper"]), 2) if pd.notna(row["bollinger_upper"]) else None,
                    bollinger_lower=round(float(row["bollinger_lower"]), 2) if pd.notna(row["bollinger_lower"]) else None,
                    fg_index=round(float(row["fg_index"]), 1) if pd.notna(row["fg_index"]) else None,
                    lag_1=round(float(row["lag_1"]), 2) if pd.notna(row["lag_1"]) else None,
                    lag_7=round(float(row["lag_7"]), 2) if pd.notna(row["lag_7"]) else None,
                )
            )

        Feature.objects.all().delete()
        Feature.objects.bulk_create(feature_objects, batch_size=1000)

        non_null_fg = Feature.objects.filter(fg_index__isnull=False).count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully computed and stored features for {len(feature_objects)} records! "
                f"Features with non-null fg_index: {non_null_fg}."
            )
        )