from django.apps import AppConfig


class MlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml'
    # No start-up model loading: models are loaded lazily on first use
    # (see model_loader.py), so `runserver` and `manage.py` start fast.
