from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import OHLCV,Feature
from .serializers import OHLCVSerializer,FeatureSerializer


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