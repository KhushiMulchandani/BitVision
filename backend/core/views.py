from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from datetime import timedelta
from django.utils import timezone
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import OHLCV,Feature,Prediction,ModelMetric,Portfolio,Alert
from .serializers import OHLCVSerializer,FeatureSerializer,PredictionSerializer,ModelMetricSerializer,PortfolioSerializer,AlertSerializer
from rest_framework.views import APIView


class OHLCVFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = OHLCV
        fields = ["start_date", "end_date"]

class FeatureFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Feature
        fields = ["start_date", "end_date"]

class OHLCVListView(generics.ListAPIView):
    """
    API endpoint that returns historical OHLCV data with optional date filtering.
    Example: /api/ohlcv/?start_date=2026-01-01&end_date=2026-06-01
    """
    queryset = OHLCV.objects.all().order_by("date")
    serializer_class = OHLCVSerializer
    filterset_class = OHLCVFilter

class FeatureListView(generics.ListAPIView):
    """
    API endpoint that returns calculated technical indicators and features.
    Example: /api/features/?start_date=2026-01-01&end_date=2026-06-01
    """
    queryset = Feature.objects.all().order_by("date")
    serializer_class = FeatureSerializer
    filterset_class = FeatureFilter

class PriceListView(generics.ListAPIView):
    """
    GET /api/price/?range=30d
    Returns historical price data from OHLCV for the last N days.
    """
    serializer_class = OHLCVSerializer

    def get_queryset(self):
        queryset = OHLCV.objects.all().order_by("date")
        range_param = self.request.query_params.get("range", None)

        if range_param and range_param.endswith("d"):
            try:
                days = int(range_param[:-1])
                # Filter for the last N days relative to the latest available date in DB
                latest_entry = OHLCV.objects.order_by("-date").first()
                if latest_entry:
                    start_date = latest_entry.date - timedelta(days=days)
                    queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass

        return queryset


class CompareListView(generics.ListAPIView):
    """
    GET /api/compare/
    Returns rows from ModelMetric for model performance evaluation/comparison.
    """
    queryset = ModelMetric.objects.all().order_by("-evaluated_at")
    serializer_class = ModelMetricSerializer


class BacktestListView(generics.ListAPIView):
    """
    GET /api/backtest/?days=30
    Returns predictions where actual_price is filled.
    """
    serializer_class = PredictionSerializer

    def get_queryset(self):
        queryset = Prediction.objects.filter(actual_price__isnull=False).order_by("date")
        days_param = self.request.query_params.get("days", None)

        if days_param:
            try:
                days = int(days_param)
                latest_prediction = Prediction.objects.filter(actual_price__isnull=False).order_by("-date").first()
                if latest_prediction:
                    start_date = latest_prediction.date - timedelta(days=days)
                    queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass

        return queryset

class PredictStubView(APIView):
    """
    GET /api/predict/
    Returns a hardcoded stub response matching the contract shape for frontend integration.
    """
    def get(self, request):
        stub_data = {
            "date": "2026-08-03",
            "predicted_price": 61500.00,
            "model_used": "stacked",
            "confidence": 0.85,
            "indicators_used": {
                "rsi_14": 58.4,
                "macd": 120.5,
                "ma_20": 60800.00
            }
        }
        return Response(stub_data)