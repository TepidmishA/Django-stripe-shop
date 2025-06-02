"""
App Configuration Module

Defines the application configuration for the 'store' Django app.
"""

from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
    Configuration class for the 'store' application.

    Sets default model primary key type and app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
