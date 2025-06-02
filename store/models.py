"""
Models Module

Defines the `Item` model used to represent products in the store application.
"""

from django.db import models


class Item(models.Model):
    """
    Represents a product with a name, optional description, and price.

    Fields:
        - name (str): The name of the item (max length: 200).
        - description (str, optional): A brief description of the item.
        - price (Decimal): The item's price with up to 10 digits and 2 decimal places.
        - currency (str): Валюта товара, например 'usd' или 'pln'.
    """
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('pln', 'PLN'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='usd'
    )

    def __str__(self):
        return f"{self.name} | {self.price}  {self.currency.upper()}"
