from django.urls import path
from .views import OHLCVListView,FeatureListView

urlpatterns = [
    path('ohlcv/', OHLCVListView.as_view(), name='ohlcv-list'),
    path("features/", FeatureListView.as_view(), name="feature-list"),
]