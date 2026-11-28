from django.contrib import admin
from .models import OHLCV, Feature, Prediction, ModelMetric, Portfolio, Alert, Trade

# Register your models here.

admin.site.register(OHLCV)
admin.site.register(Feature)
admin.site.register(Prediction)
admin.site.register(ModelMetric)
admin.site.register(Portfolio)
admin.site.register(Alert)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ("user", "side", "usd_amount", "btc_amount", "price", "created_at")
    list_filter = ("side",)