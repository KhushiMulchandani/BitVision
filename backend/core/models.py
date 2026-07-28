from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class OHLCV(models.Model):
    date = models.DateField(unique=True)
    open = models.DecimalField(max_digits=12, decimal_places=2)
    high = models.DecimalField(max_digits=12, decimal_places=2)
    low = models.DecimalField(max_digits=12, decimal_places=2)
    close = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.date} close: {self.close}"


class Feature(models.Model):
    date = models.DateField(unique=True)
    rsi_14 = models.FloatField(null=True, blank=True)
    macd = models.FloatField(null=True, blank=True)
    macd_signal = models.FloatField(null=True, blank=True)
    ma_20 = models.FloatField(null=True, blank=True)
    ma_50 = models.FloatField(null=True, blank=True)
    bollinger_upper = models.FloatField(null=True, blank=True)
    bollinger_lower = models.FloatField(null=True, blank=True)
    fg_index = models.FloatField(null=True, blank=True)
    lag_1 = models.FloatField(null=True, blank=True)
    lag_7 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Features - {self.date}"


class Prediction(models.Model):
    date = models.DateField()
    predicted_price = models.DecimalField(max_digits=12, decimal_places=2)
    actual_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    model_used = models.CharField(max_length=20)  # "rf" / "xgb" / "lstm" / "stacked"
    confidence = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("date", "model_used")

    def __str__(self):
        return f"{self.model_used} Prediction - {self.date}"


class ModelMetric(models.Model):
    model_name = models.CharField(max_length=20)
    rmse = models.FloatField()
    mae = models.FloatField()
    mape = models.FloatField()
    directional_accuracy = models.FloatField()
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metrics - {self.model_name}"


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)
    btc_holdings = models.DecimalField(max_digits=16, decimal_places=8, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Portfolio ({self.user.username})"


class Alert(models.Model):
    DIRECTION_CHOICES = [
        ("above", "Above"),
        ("below", "Below"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_price = models.DecimalField(max_digits=12, decimal_places=2)
    direction = models.CharField(max_length=5, choices=DIRECTION_CHOICES)
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert: {self.direction} {self.target_price} ({self.user.username})"