from django.apps import AppConfig


class MueblesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'muebles'

    def ready(self):
        import muebles.signals
