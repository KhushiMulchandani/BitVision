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
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from decimal import Decimal

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

# class PriceListView(generics.ListAPIView):
#     """
#     GET /api/price/?range=30d
#     Returns historical price data from OHLCV for the last N days.
#     """
#     serializer_class = OHLCVSerializer

#     def get_queryset(self):
#         queryset = OHLCV.objects.all().order_by("date")
#         range_param = self.request.query_params.get("range", None)

#         if range_param and range_param.endswith("d"):
#             try:
#                 days = int(range_param[:-1])
#                 # Filter for the last N days relative to the latest available date in DB
#                 latest_entry = OHLCV.objects.order_by("-date").first()
#                 if latest_entry:
#                     start_date = latest_entry.date - timedelta(days=days)
#                     queryset = queryset.filter(date__gte=start_date)
#             except ValueError:
#                 pass

#         return queryset


# class CompareListView(generics.ListAPIView):
#     """
#     GET /api/compare/
#     Returns rows from ModelMetric for model performance evaluation/comparison.
#     """
#     queryset = ModelMetric.objects.all().order_by("-evaluated_at")
#     serializer_class = ModelMetricSerializer


# class BacktestListView(generics.ListAPIView):
#     """
#     GET /api/backtest/?days=30
#     Returns predictions where actual_price is filled.
#     """
#     serializer_class = PredictionSerializer

#     def get_queryset(self):
#         queryset = Prediction.objects.filter(actual_price__isnull=False).order_by("date")
#         days_param = self.request.query_params.get("days", None)

#         if days_param:
#             try:
#                 days = int(days_param)
#                 latest_prediction = Prediction.objects.filter(actual_price__isnull=False).order_by("-date").first()
#                 if latest_prediction:
#                     start_date = latest_prediction.date - timedelta(days=days)
#                     queryset = queryset.filter(date__gte=start_date)
#             except ValueError:
#                 pass

#         return queryset

# class PredictStubView(APIView):
#     """
#     GET /api/predict/
#     Returns a hardcoded stub response matching the contract shape for frontend integration.
#     """
#     def get(self, request):
#         stub_data = {
#             "date": "2026-08-03",
#             "predicted_price": 61500.00,
#             "model_used": "stacked",
#             "confidence": 0.85,
#             "indicators_used": {
#                 "rsi_14": 58.4,
#                 "macd": 120.5,
#                 "ma_20": 60800.00
#             }
#         }
#         return Response(stub_data)

# class PortfolioView(APIView):
#     """
#     GET /api/portfolio/ - Retrieve current user portfolio (auto-creates if missing).
#     POST /api/portfolio/ - Buy/Sell BTC using paper trading cash.
#     """
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         portfolio, created = Portfolio.objects.get_or_create(user=request.user)
#         serializer = PortfolioSerializer(portfolio)
#         return Response(serializer.data)

#     def post(self, request):
#         portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
#         action = request.data.get("action")
#         amount_inr = request.data.get("amount_inr")

#         if not action or amount_inr is None:
#             return Response(
#                 {"error": "Both 'action' and 'amount_inr' are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             amount_inr = Decimal(str(amount_inr))
#             if amount_inr <= 0:
#                 return Response(
#                     {"error": "Amount must be greater than zero."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         except Exception:
#             return Response(
#                 {"error": "Invalid amount provided."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Get latest BTC price from OHLCV table
#         latest_entry = OHLCV.objects.order_by("-date").first()
#         if not latest_entry:
#             return Response(
#                 {"error": "No market data available to perform trade."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         btc_price = latest_entry.close  # Price in USD/INR

#         if action == "buy":
#             if portfolio.cash_balance < amount_inr:
#                 return Response(
#                     {"error": "Insufficient cash balance."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             btc_purchased = amount_inr / btc_price
#             portfolio.cash_balance -= amount_inr
#             portfolio.btc_holdings += btc_purchased
#             portfolio.save()

#         elif action == "sell":
#             btc_to_sell = amount_inr / btc_price
#             if portfolio.btc_holdings < btc_to_sell:
#                 return Response(
#                     {"error": "Insufficient BTC holdings to sell."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             portfolio.cash_balance += amount_inr
#             portfolio.btc_holdings -= btc_to_sell
#             portfolio.save()

#         else:
#             return Response(
#                 {"error": "Invalid action. Use 'buy' or 'sell'."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         serializer = PortfolioSerializer(portfolio)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class AlertListCreateView(generics.ListCreateAPIView):
#     """
#     GET /api/alerts/ - List active user alerts.
#     POST /api/alerts/ - Create new price alert target.
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = AlertSerializer

#     def get_queryset(self):
#         return Alert.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class PriceListView(generics.ListAPIView):
    """
    GET /api/price/?range=30d
    Returns historical price data from OHLCV for the last N days.
    """
    serializer_class = OHLCVSerializer

    def get_queryset(self):
        try:
            queryset = OHLCV.objects.all().order_by("date")
            range_param = self.request.query_params.get("range", None)

            if range_param and range_param.endswith("d"):
                try:
                    days = int(range_param[:-1])
                    if days > 0:
                        latest_entry = OHLCV.objects.order_by("-date").first()
                        if latest_entry:
                            start_date = latest_entry.date - timedelta(days=days)
                            queryset = queryset.filter(date__gte=start_date)
                except ValueError:
                    pass

            return queryset
        except Exception:
            return OHLCV.objects.none()


class CompareListView(generics.ListAPIView):
    """
    GET /api/compare/
    Returns rows from ModelMetric for model evaluation/comparison.
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
        try:
            queryset = Prediction.objects.filter(actual_price__isnull=False).order_by("date")
            days_param = self.request.query_params.get("days", None)

            if days_param:
                try:
                    days = int(days_param)
                    if days > 0:
                        latest_prediction = Prediction.objects.filter(actual_price__isnull=False).order_by("-date").first()
                        if latest_prediction:
                            start_date = latest_prediction.date - timedelta(days=days)
                            queryset = queryset.filter(date__gte=start_date)
                except ValueError:
                    pass

            return queryset
        except Exception:
            return Prediction.objects.none()


class PredictStubView(APIView):
    """
    GET /api/predict/
    Returns contract-compliant stub data until ML model artifacts are loaded.
    """
    def get(self, request):
        try:
            stub_data = {
                "date": "2026-08-03",
                "predicted_price": 61500.00,
                "model_used": "stacked",
                "confidence": 0.85,
                "indicators_used": {
                    "rsi_14": 58.4,
                    "macd": 120.5,
                    "ma_20": 60800.00,
                },
            }
            return Response(stub_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Failed to generate prediction data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PortfolioView(APIView):
    """
    GET /api/portfolio/ - Retrieve current user portfolio (auto-creates if missing).
    POST /api/portfolio/ - Buy/Sell BTC using paper trading cash.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            portfolio, created = Portfolio.objects.get_or_create(user=request.user)
            serializer = PortfolioSerializer(portfolio)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Could not retrieve portfolio", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        try:
            portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
            action = request.data.get("action")
            amount_inr = request.data.get("amount_inr")

            # 1. Required Field Validation
            if not action or amount_inr is None:
                return Response(
                    {"error": "Both 'action' and 'amount_inr' fields are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 2. Action Field Validation
            action = str(action).lower().strip()
            if action not in ["buy", "sell"]:
                return Response(
                    {"error": "Invalid action. Allowed choices are 'buy' or 'sell'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 3. Numeric Amount & Non-negative Validation
            try:
                amount_inr = Decimal(str(amount_inr))
                if amount_inr <= Decimal("0"):
                    return Response(
                        {"error": "Amount must be greater than zero."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except (InvalidOperation, TypeError, ValueError):
                return Response(
                    {"error": "Invalid amount provided. Must be a positive numeric value."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 4. Fetch Market Data
            latest_entry = OHLCV.objects.order_by("-date").first()
            if not latest_entry or latest_entry.close <= Decimal("0"):
                return Response(
                    {"error": "Market data currently unavailable for trading calculation."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            btc_price = latest_entry.close

            # 5. Trading Execution
            if action == "buy":
                if portfolio.cash_balance < amount_inr:
                    return Response(
                        {
                            "error": "Insufficient funds.",
                            "current_balance": str(portfolio.cash_balance),
                            "requested": str(amount_inr),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                btc_purchased = amount_inr / btc_price
                portfolio.cash_balance -= amount_inr
                portfolio.btc_holdings += btc_purchased
                portfolio.save()

            elif action == "sell":
                btc_to_sell = amount_inr / btc_price
                if portfolio.btc_holdings < btc_to_sell:
                    return Response(
                        {
                            "error": "Insufficient BTC holdings to complete sell order.",
                            "current_holdings": str(portfolio.btc_holdings),
                            "requested_btc": str(btc_to_sell),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                portfolio.cash_balance += amount_inr
                portfolio.btc_holdings -= btc_to_sell
                portfolio.save()

            serializer = PortfolioSerializer(portfolio)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "An internal server error occurred while processing transaction.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AlertListCreateView(generics.ListCreateAPIView):
    """
    GET /api/alerts/ - List active user alerts.
    POST /api/alerts/ - Create new price alert target.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer

    def get_queryset(self):
        try:
            return Alert.objects.filter(user=self.request.user)
        except Exception:
            return Alert.objects.none()

    def create(self, request, *args, **kwargs):
        target_price = request.data.get("target_price")
        direction = request.data.get("direction")

        # Input validation for create
        if target_price is None or direction is None:
            return Response(
                {"error": "Both 'target_price' and 'direction' fields are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            target_price_dec = Decimal(str(target_price))
            if target_price_dec <= Decimal("0"):
                return Response(
                    {"error": "target_price must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (InvalidOperation, TypeError, ValueError):
            return Response(
                {"error": "Invalid target_price format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if str(direction).lower().strip() not in ["above", "below"]:
            return Response(
                {"error": "direction must be 'above' or 'below'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)