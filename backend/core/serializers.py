from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .services import MODEL_LABELS

from decimal import Decimal
from .models import OHLCV, Feature, Prediction, ModelMetric, Portfolio, Alert, Trade

STARTING_CASH = Decimal("10000.00")
CENT = Decimal("0.01")

class OHLCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = OHLCV
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = "__all__"


class ModelMetricSerializer(serializers.ModelSerializer):
    is_baseline = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()

    class Meta:
        model = ModelMetric
        fields = "__all__"

    def get_is_baseline(self, obj):
        return obj.model_name == "baseline"

    def get_label(self, obj):
        return MODEL_LABELS.get(obj.model_name, obj.model_name)

    def get_note(self, obj):
        if obj.model_name == "baseline":
            return "Directional accuracy here is the share of up-days, not a model's call."
        return None

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ("cash_balance", "btc_holdings", "updated_at")

    def to_representation(self, obj):
        data = super().to_representation(obj)
        cash = Decimal(str(obj.cash_balance))
        btc = Decimal(str(obj.btc_holdings))
        latest = OHLCV.objects.order_by("-date").first()
        price = latest.close if latest else None
        holdings = (btc * price).quantize(CENT) if price else None
        total = (cash + holdings).quantize(CENT) if holdings is not None else None
        data.update({
            "currency": "USD",
            "starting_balance": str(STARTING_CASH),
            "latest_price": str(price) if price else None,
            "holdings_value": str(holdings) if holdings is not None else None,
            "total_value": str(total) if total is not None else None,
            "profit_loss": str((total - STARTING_CASH).quantize(CENT)) if total is not None else None,
        })
        return data


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = ("id", "side", "usd_amount", "btc_amount", "price", "created_at")


class TradeRequestSerializer(serializers.Serializer):
    action = serializers.CharField()
    amount_usd = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0.01"), required=False)
    amount_inr = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal("0.01"), required=False)  # deprecated alias

    def validate_action(self, value):
        value = value.lower().strip()
        if value not in ("buy", "sell"):
            raise serializers.ValidationError("Must be 'buy' or 'sell'.")
        return value

    def validate(self, attrs):
        usd, legacy = attrs.get("amount_usd"), attrs.get("amount_inr")
        if usd is None and legacy is None:
            raise serializers.ValidationError({"amount_usd": "This field is required."})
        attrs["amount"] = usd if usd is not None else legacy
        attrs["used_legacy"] = usd is None
        return attrs


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ("id", "target_price", "direction", "is_triggered", "triggered_at", "created_at")
        read_only_fields = ("is_triggered", "triggered_at", "created_at")

    def validate_target_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Must be greater than zero.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value.lower()

    def validate(self, attrs):
        user = User(username=attrs["username"], email=attrs["email"])
        try:
            validate_password(attrs["password"], user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)