from django.urls import path
from .views import (OHLCVListView, FeatureListView, PriceListView, CompareListView, BacktestListView,
                    PredictView, PortfolioView, AlertListCreateView, SentimentView, RegisterView, AlertListCreateView, AlertDetailView, TradeListView, MeView)

urlpatterns = [
    path("ohlcv/", OHLCVListView.as_view(), name="ohlcv-list"),
    path("features/", FeatureListView.as_view(), name="feature-list"),
    path("price/", PriceListView.as_view(), name="price-list"),
    path("compare/", CompareListView.as_view(), name="compare-list"),
    path("backtest/", BacktestListView.as_view(), name="backtest-list"),
    path("predict/", PredictView.as_view(), name="predict"),
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("alerts/", AlertListCreateView.as_view(), name="alert-list-create"),
    path("sentiment/", SentimentView.as_view(), name="sentiment"),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("trades/", TradeListView.as_view(), name="trade-list"),
    path("alerts/<int:pk>/", AlertDetailView.as_view(), name="alert-detail"),
]