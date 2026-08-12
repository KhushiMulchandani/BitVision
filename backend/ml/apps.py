from django.apps import AppConfig

class MlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml'

    def ready(self):
        # Trigger model loading on startup
        from .model_loader import MLModelLoader
        try:
            MLModelLoader.get_lstm_model()
        except Exception as e:
            print(f"Warning: Could not preload ML model on startup: {e}")