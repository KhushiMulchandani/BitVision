from django.urls import path
from .views import (OHLCVListView,FeatureListView,PriceListView,CompareListView,BacktestListView,PredictStubView,PortfolioView,AlertListCreateView,SentimentView,)

urlpatterns = [
    path('ohlcv/', OHLCVListView.as_view(), name='ohlcv-list'),
    path("features/", FeatureListView.as_view(), name="feature-list"),
    path("price/", PriceListView.as_view(), name="price-list"),
    path("compare/", CompareListView.as_view(), name="compare-list"),
    path("backtest/", BacktestListView.as_view(), name="backtest-list"),
    path("predict/", PredictStubView.as_view(), name="predict-stub"),
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("alerts/", AlertListCreateView.as_view(), name="alert-list-create"),
    path("sentiment/", SentimentView.as_view(), name="sentiment"),
]