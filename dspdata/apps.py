from django.apps import AppConfig


class DspdataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dspdata'

    def ready(self):
        super().ready()


