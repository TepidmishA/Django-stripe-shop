"""
Admin Module

Registers the `Item` model with the Django admin site
to enable management through the admin interface.
"""

from django.contrib import admin

from .models import Item

admin.site.register(Item)
