from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import OHLCV, Feature, Prediction, ModelMetric, Portfolio, Alert
from .services import MODEL_LABELS


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
        fields = "__all__"


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"


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