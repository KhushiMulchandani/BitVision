from django.urls import path
from .views import OHLCVListView,FeatureListView,PriceListView,CompareListView,BacktestListView,PredictStubView

urlpatterns = [
    path('ohlcv/', OHLCVListView.as_view(), name='ohlcv-list'),
    path("features/", FeatureListView.as_view(), name="feature-list"),
    # Stage 6 Read-only routes for Frontend Integration
    path("price/", PriceListView.as_view(), name="price-list"),
    path("compare/", CompareListView.as_view(), name="compare-list"),
    path("backtest/", BacktestListView.as_view(), name="backtest-list"),
    # Stage 7 Prediction Stub route
    path("predict/", PredictStubView.as_view(), name="predict-stub"),
]