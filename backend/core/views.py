from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import OHLCV
from .serializers import OHLCVSerializer


class OHLCVListView(generics.ListAPIView):
    """
    API endpoint that returns historical OHLCV data.
    """
    queryset = OHLCV.objects.all().order_by("date")
    serializer_class = OHLCVSerializer