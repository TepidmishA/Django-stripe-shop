"""
Admin Module

Registers the `Item` model with the Django admin site
to enable management through the admin interface.
"""

from django.contrib import admin

from .models import Item, Discount, Tax, Order

admin.site.register(Item)
admin.site.register(Discount)
admin.site.register(Tax)
admin.site.register(Order)
