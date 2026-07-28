from django.contrib import admin
from .models import OHLCV, Feature, Prediction, ModelMetric, Portfolio, Alert

# Register your models here.

admin.site.register(OHLCV)
admin.site.register(Feature)
admin.site.register(Prediction)
admin.site.register(ModelMetric)
admin.site.register(Portfolio)
admin.site.register(Alert)