from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'africonnect.profiles'

    def ready(self):
        import africonnect.profiles.signals
