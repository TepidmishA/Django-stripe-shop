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


class Discount(models.Model):
    """
    A fixed discount percentage that can be attached to an Order.

    Fields:
        - code (str): A unique discount code, e.g., "SAVE10".
        - percentage (Decimal): Discount value in the same currency as the order (e.g., 10.00).
    """
    code = models.CharField(max_length=50, unique=True)
    percentage = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.code} — {self.percentage}"


class Tax(models.Model):
    """
    A tax (percentage-based) that can be applied to an Order.

    Fields:
        - name (str): The name of the tax, e.g., "VAT".
        - percentage (Decimal): The tax percentage (e.g., 5.00 means 5%).
    """
    name = models.CharField(max_length=50)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.name} — {self.percentage}%"


class Order(models.Model):
    """
    An order consisting of multiple items, with optional discount and tax.

    Fields:
        - items (ManyToMany to Item): List of items in the order.
        - discount (ForeignKey to Discount, nullable): Applied discount (optional).
        - tax (ForeignKey to Tax, nullable): Applied tax (optional).
        - created_at (DateTime): Timestamp when the order was created.
    """
    items = models.ManyToManyField(
        Item,
        related_name='orders'
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tax = models.ForeignKey(
        Tax,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} — {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def subtotal(self):
        """
        Returns the total price of all items without applying discounts or taxes.
        """
        return sum(item.price for item in self.items.all())

    def discount_amount(self):
        """
        Returns the discount amount. Returns 0 if no discount is applied.
        """
        base = self.subtotal()
        amount = base * (self.discount.percentage / 100) if self.discount else 0
        return round(amount, 2)

    def tax_amount(self):
        """
        Returns the calculated tax amount:
        (subtotal - discount) * (tax percentage / 100).
        Returns 0 if no tax is applied.
        """
        base = self.subtotal() - self.discount_amount()
        amount = base * (self.tax.percentage / 100) if self.tax else 0
        return round(amount, 2)

    def total_amount(self):
        """
        Returns the final total amount after applying discount and tax.
        """
        return self.subtotal() - self.discount_amount() + self.tax_amount()

    def currency(self):
        """
        Assumes all items in the order share the same currency.
        Returns the currency of the first item, or 'usd' if the order is empty.
        """
        first_item = self.items.first()
        return first_item.currency if first_item else 'usd'
