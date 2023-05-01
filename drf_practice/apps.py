from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DrfPracticeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drf_practice'

    def ready(self):
        import drf_practice.signals
