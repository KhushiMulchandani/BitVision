from django.apps import AppConfig

class MlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml'

    def ready(self):
        # Models are loaded lazily on first inference request to keep startup fast
        pass