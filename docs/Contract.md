# The Contract — Matched to Prof. Vishal Acharya's Spec

Rebuilt directly from your professor's HTML file. A few corrections from the earlier version:
your professor asks for **6 database tables**, not 3 (I'd missed `ModelMetric`, `Portfolio`, `Alert`);
endpoint URLs are **singular** (`/api/price/`, not `/api/prices/`); and the feature columns are a
specific, smaller list than what I gave you before. This version matches his Day 2 / Day 4 / Day 5
checkpoints exactly, so use this one.

---

## Part 1: Database Tables — All 6, As Named in the Roadmap

Your professor's Day 2 checkpoint literally says: *"Create 6 models: OHLCV, Feature, Prediction,
ModelMetric, Portfolio, Alert."* Use these exact names — it'll match what he expects to see in your
Django admin panel.

### 1. `OHLCV` — raw daily price data
| Field | Type | Meaning |
|---|---|---|
| `date` | Date | Which day |
| `open` / `high` / `low` / `close` | Decimal | Standard daily candle prices |
| `volume` | Big number | Trading volume that day |

### 2. `Feature` — technical indicators (per Day 4 & Day 5 checkpoints, exact list)
| Field | Meaning |
|---|---|
| `date` | Which day this row's indicators are for |
| `rsi_14` | RSI over 14 days — overbought/oversold signal |
| `macd` | MACD line |
| `macd_signal` | MACD signal line (needed to compare against `macd`) |
| `ma_20` / `ma_50` | 20-day and 50-day moving averages (professor specifies 20/50, not 7/21) |
| `bollinger_upper` / `bollinger_lower` | Volatility bands |
| `fg_index` | Fear & Greed Index score, 0-100 — **this exact column name** is called out in the Day 5 checkpoint |
| `lag_1` / `lag_7` | Yesterday's close, and close from 7 days ago — used so the model has direct memory of recent price without leaking future info |

### 3. `Prediction` — model outputs
| Field | Meaning |
|---|---|
| `date` | Day the prediction is for |
| `predicted_price` | The forecast |
| `actual_price` | Filled in later once known (nullable) |
| `model_used` | `"rf"` / `"xgb"` / `"lstm"` / `"stacked"` |
| `confidence` | Optional 0-1 score |

### 4. `ModelMetric` — the comparison table (Day 13 checkpoint: "a clean 4×4 metrics table")
| Field | Meaning |
|---|---|
| `model_name` | `"rf"` / `"xgb"` / `"lstm"` / `"stacked"` |
| `rmse` | Typical dollar error, penalizes big misses |
| `mae` | Average dollar error |
| `mape` | Average % error |
| `directional_accuracy` | % of days the model got the up/down direction right |
| `evaluated_at` | Timestamp, so you can track metrics over retrains |

### 5. `Portfolio` — paper trading (Feature 7: "Virtual ₹10,000 wallet")
| Field | Meaning |
|---|---|
| `user` | Link to the logged-in student (each user gets their own portfolio — Feature 8) |
| `cash_balance` | Starts at 10000, changes as they "trade" |
| `btc_holdings` | How much BTC they're virtually holding |
| `updated_at` | Last trade timestamp |

### 6. `Alert` — price alerts (implied by the table name; not detailed further in the roadmap, so this is a reasonable minimal version — confirm with your professor if he wants something specific here)
| Field | Meaning |
|---|---|
| `user` | Who set the alert |
| `target_price` | The price to watch for |
| `direction` | `"above"` or `"below"` |
| `is_triggered` | Boolean, flips once hit |
| `created_at` | Timestamp |

---

## Part 2: API Endpoints — Exact URLs From the Architecture Diagram

Your professor's Layer 2 diagram lists these **exact paths** — note they're singular (`price`, not `prices`):

### Auth (SimpleJWT — needed for Feature 8, login)
```
POST /api/token/          → {"username": "...", "password": "..."}
                           → {"access": "...", "refresh": "..."}
POST /api/token/refresh/  → {"refresh": "..."}  → {"access": "..."}
```

### 1. `GET /api/price/?range=30d`
**"GET latest + history"** — powers Feature 1 (Live Price Dashboard).
```json
[
  {"date": "2026-06-25", "open": 61500, "high": 62800, "low": 61000, "close": 62300, "volume": 28450000000},
  {"date": "2026-06-26", "open": 62300, "high": 63100, "low": 61800, "close": 62900, "volume": 26120000000}
]
```

### 2. `GET /api/predict/`
**"Tomorrow's price"** — powers Feature 2.
```json
{
  "date": "2026-07-27",
  "predicted_price": 63450.20,
  "confidence": 0.78,
  "model_breakdown": {
    "rf": 63100.00,
    "xgb": 63600.50,
    "lstm": 63550.00,
    "stacked": 63450.20
  }
}
```

### 3. `GET /api/compare/`
**"All model metrics"** — powers Feature 3, pulled straight from the `ModelMetric` table.
```json
{
  "rf":      {"rmse": 890.5, "mae": 650.2, "mape": 1.42, "directional_accuracy": 0.61},
  "xgb":     {"rmse": 820.1, "mae": 600.7, "mape": 1.31, "directional_accuracy": 0.64},
  "lstm":    {"rmse": 950.3, "mae": 700.4, "mape": 1.55, "directional_accuracy": 0.58},
  "stacked": {"rmse": 760.0, "mae": 540.8, "mape": 1.18, "directional_accuracy": 0.68}
}
```

### 4. `GET /api/backtest/?days=30`
**"Last-30-day accuracy"** — powers Feature 6.
```json
[
  {"date": "2026-06-27", "actual": 62100, "predicted": 61950, "model": "stacked"},
  {"date": "2026-06-28", "actual": 62450, "predicted": 62600, "model": "stacked"}
]
```

### 5. `/api/portfolio/` (GET + POST — "Paper trades CRUD")
**GET** → current state:
```json
{"cash_balance": 8500.00, "btc_holdings": 0.021, "current_value": 9812.30, "profit_loss_pct": -1.87}
```
**POST** → place a paper trade:
```json
{"action": "buy", "amount_inr": 1500}
```

---

## Part 3: Starting Code — Matched to This Spec

### `backend/core/models.py`
```python
from django.db import models
from django.contrib.auth.models import User


class OHLCV(models.Model):
    date = models.DateField(unique=True)
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.date} - close: {self.close}"


class Feature(models.Model):
    date = models.DateField(unique=True)
    rsi_14 = models.FloatField(null=True)
    macd = models.FloatField(null=True)
    macd_signal = models.FloatField(null=True)
    ma_20 = models.FloatField(null=True)
    ma_50 = models.FloatField(null=True)
    bollinger_upper = models.FloatField(null=True)
    bollinger_lower = models.FloatField(null=True)
    fg_index = models.FloatField(null=True)
    lag_1 = models.FloatField(null=True)
    lag_7 = models.FloatField(null=True)


class Prediction(models.Model):
    date = models.DateField()
    predicted_price = models.DecimalField(max_digits=12, decimal_places=2)
    actual_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    model_used = models.CharField(max_length=20)  # rf / xgb / lstm / stacked
    confidence = models.FloatField(null=True, blank=True)


class ModelMetric(models.Model):
    model_name = models.CharField(max_length=20)
    rmse = models.FloatField()
    mae = models.FloatField()
    mape = models.FloatField()
    directional_accuracy = models.FloatField()
    evaluated_at = models.DateTimeField(auto_now_add=True)


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)
    btc_holdings = models.DecimalField(max_digits=16, decimal_places=8, default=0)
    updated_at = models.DateTimeField(auto_now=True)


class Alert(models.Model):
    DIRECTION_CHOICES = [("above", "Above"), ("below", "Below")]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES)
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```
Then:
```bash
python manage.py makemigrations
python manage.py migrate
```
Register all 6 in `admin.py` (per Day 2 checkpoint — "All 6 tables visible in Django admin"):
```python
from django.contrib import admin
from .models import OHLCV, Feature, Prediction, ModelMetric, Portfolio, Alert

admin.site.register(OHLCV)
admin.site.register(Feature)
admin.site.register(Prediction)
admin.site.register(ModelMetric)
admin.site.register(Portfolio)
admin.site.register(Alert)
```

### `frontend/src/api/mockData.js`
```javascript
export const mockPrice = [
  { date: "2026-06-25", open: 61500, high: 62800, low: 61000, close: 62300, volume: 28450000000 },
  { date: "2026-06-26", open: 62300, high: 63100, low: 61800, close: 62900, volume: 26120000000 },
];

export const mockPrediction = {
  date: "2026-07-27",
  predicted_price: 63450.20,
  confidence: 0.78,
  model_breakdown: { rf: 63100.00, xgb: 63600.50, lstm: 63550.00, stacked: 63450.20 }
};

export const mockCompare = {
  rf:      { rmse: 890.5, mae: 650.2, mape: 1.42, directional_accuracy: 0.61 },
  xgb:     { rmse: 820.1, mae: 600.7, mape: 1.31, directional_accuracy: 0.64 },
  lstm:    { rmse: 950.3, mae: 700.4, mape: 1.55, directional_accuracy: 0.58 },
  stacked: { rmse: 760.0, mae: 540.8, mape: 1.18, directional_accuracy: 0.68 }
};

export const mockPortfolio = {
  cash_balance: 8500.00, btc_holdings: 0.021, current_value: 9812.30, profit_loss_pct: -1.87
};
```

---

## What Changed From the Earlier Version — Quick Diff

| Before | Now (matches professor) |
|---|---|
| 3 tables | **6 tables**: OHLCV, Feature, Prediction, ModelMetric, Portfolio, Alert |
| `sma_7`/`sma_21`/`ema_12` | `ma_20`/`ma_50` (no EMA — not in his spec) |
| `fear_greed_index` | `fg_index` (his exact naming) |
| No lag features | `lag_1`, `lag_7` added |
| `/api/prices/` | `/api/price/` (singular) |
| No auth endpoints | `/api/token/`, `/api/token/refresh/` (SimpleJWT, needed for Feature 8) |
| No portfolio/metric detail | `ModelMetric` and `Portfolio` fully specified per Feature 3 & 7 |

Everything else from before (the Day 0 meeting agenda, the reasoning for why contract-first matters) still applies exactly as-is — only the actual field names and URLs are corrected here.
