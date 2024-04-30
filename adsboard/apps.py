from django.apps import AppConfig


class AdsboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adsboard'

    def ready(self):
        from . import signals
