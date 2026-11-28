from django.test import TestCase

# Create your tests here.
from datetime import date
from unittest import mock

from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.test import APITestCase

from core.models import OHLCV, ModelMetric, Portfolio, Prediction
from ml.model_loader import ModelsNotTrained

PRICES = {"rf": 80100, "xgb": 80200, "lstm": 79900, "stacked": 80150}
PASSWORD = "Str0ng!Pass_2026"


def _result(pred_date, close=80000.0):
    models = {c: {"predicted_return": p / close - 1, "predicted_price": float(p), "lower_price": p - 1500.0,
                  "upper_price": p + 1500.0, "confidence": 0.87} for c, p in PRICES.items()}
    return {"based_on_date": "2026-11-20", "date": pred_date, "current_close": close,
            "direction": "up", "models": models}


class AuthTests(APITestCase):
    def setUp(self):
        cache.clear()      # throttle counters live in the cache

    def _register(self, **over):
        data = {"username": "khushi", "email": "k@example.com", "password": PASSWORD, **over}
        return self.client.post("/api/register/", data, format="json")

    def test_register_returns_user_and_tokens(self):
        r = self._register()
        self.assertEqual(r.status_code, 201)
        self.assertIn("access", r.data)
        self.assertIn("refresh", r.data)
        self.assertEqual(r.data["user"]["email"], "k@example.com")
        self.assertTrue(Portfolio.objects.filter(user__username="khushi").exists())

    def test_duplicate_username_and_email_rejected(self):
        self._register()
        self.assertEqual(self._register(email="other@example.com").status_code, 400)
        self.assertEqual(self._register(username="other", email="K@Example.com").status_code, 400)

    def test_weak_password_rejected(self):
        r = self._register(password="12345678")
        self.assertEqual(r.status_code, 400)
        self.assertIn("password", r.data["details"])

    def test_me_requires_auth_and_uses_error_format(self):
        r = self.client.get("/api/me/")
        self.assertEqual(r.status_code, 401)
        self.assertIn("error", r.data)

    def test_me_with_token(self):
        token = self._register().data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = self.client.get("/api/me/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "khushi")

    def test_login_is_throttled(self):
        User.objects.create_user("u", "u@example.com", PASSWORD)
        for _ in range(5):
            r = self.client.post("/api/token/", {"username": "u", "password": "wrong"}, format="json")
            self.assertEqual(r.status_code, 401)
        r = self.client.post("/api/token/", {"username": "u", "password": PASSWORD}, format="json")
        self.assertEqual(r.status_code, 429)


class PredictViewTests(APITestCase):
    url = "/api/predict/"

    def setUp(self):
        OHLCV.objects.create(date=date(2026, 11, 20), open=79000, high=81000, low=78500, close=80000, volume=1000)
        p = mock.patch("core.services.MLModelLoader.get_metrics",
                       return_value={"meta_weights": {"rf": 0.0, "xgb": 0.32, "lstm": 0.27}})
        p.start()
        self.addCleanup(p.stop)

    def _store(self, day, stacked=80150):
        for code, price in {**PRICES, "stacked": stacked}.items():
            Prediction.objects.create(date=day, model_used=code, predicted_price=price,
                                      lower_price=price - 1500, upper_price=price + 1500, confidence=0.87)

    def test_serves_stored_rows_without_inference(self):
        self._store(date(2026, 11, 21))
        with mock.patch("core.services.predict_latest") as live:
            r = self.client.get(self.url)
        live.assert_not_called()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["direction"], "up")
        self.assertFalse(r.data["stale"])
        self.assertEqual(set(r.data["models"]), {"rf", "xgb", "lstm", "stacked"})
        self.assertEqual(r.data["baseline"]["predicted_price"], 80000.0)
        self.assertEqual(r.data["ensemble_weights"]["xgb"], 0.32)
        self.assertEqual(r.data["currency"], "USD")

    def test_direction_down(self):
        self._store(date(2026, 11, 21), stacked=79000)
        self.assertEqual(self.client.get(self.url).data["direction"], "down")

    def test_live_fallback_when_nothing_stored(self):
        with mock.patch("core.services.predict_latest", return_value=_result("2026-11-21")) as live:
            r = self.client.get(self.url)
        live.assert_called_once()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Prediction.objects.filter(date="2026-11-21").count(), 4)

    def test_503_when_no_data_and_models_missing(self):
        with mock.patch("core.services.predict_latest", side_effect=ModelsNotTrained("not trained")):
            r = self.client.get(self.url)
        self.assertEqual(r.status_code, 503)
        self.assertIn("error", r.data)

    def test_stale_flag_when_only_old_rows_exist(self):
        self._store(date(2026, 11, 19))
        with mock.patch("core.services.predict_latest", side_effect=ModelsNotTrained("x")):
            r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.data["stale"])
        self.assertEqual(r.data["date"], "2026-11-19")


class CompareBacktestTests(APITestCase):
    def test_compare_flags_baseline_and_sorts_it_last(self):
        for name, rmse in (("baseline", 1938.8), ("rf", 1953.9), ("xgb", 1959.9), ("lstm", 1955.9), ("stacked", 1949.1)):
            ModelMetric.objects.create(model_name=name, rmse=rmse, mae=1, mape=1, directional_accuracy=50)
        rows = self.client.get("/api/compare/").data["results"]
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[0]["model_name"], "stacked")
        self.assertEqual(rows[-1]["model_name"], "baseline")
        self.assertTrue(rows[-1]["is_baseline"])
        self.assertTrue(rows[-1]["note"])
        self.assertFalse(rows[0]["is_baseline"])
        self.assertEqual(rows[0]["label"], "Stacked Ensemble (Ridge)")

    def test_backtest_model_filter_and_page_size(self):
        for day in range(1, 21):
            for code in PRICES:
                Prediction.objects.create(date=date(2026, 1, day), model_used=code, predicted_price=100,
                                          actual_price=101)
        r = self.client.get("/api/backtest/?model=stacked&page_size=1000")
        self.assertEqual(r.data["count"], 20)
        self.assertTrue(all(x["model_used"] == "stacked" for x in r.data["results"]))
        self.assertEqual(self.client.get("/api/backtest/").data["count"], 80)
        self.assertEqual(self.client.get("/api/backtest/?model=stacked&days=5").data["count"], 6)