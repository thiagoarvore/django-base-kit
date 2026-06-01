from django.apps import AppConfig


class BaseKitConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_base_kit"
    label = "base_kit"
    verbose_name = "Base Kit"
