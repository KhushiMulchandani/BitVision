from django.urls import path
from .views import OHLCVListView

urlpatterns = [
    path('ohlcv/', OHLCVListView.as_view(), name='ohlcv-list'),
]