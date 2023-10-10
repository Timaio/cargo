from django.apps import AppConfig
from django.core import management
from django.db.models.signals import post_migrate


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
