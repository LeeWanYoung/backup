from django.apps import AppConfig
from django.conf import settings

class GongsaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Gongsa"
    
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from . import runapscheduler
            runapscheduler.start()
