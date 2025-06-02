"""
Store Views Module

Implements view functions for displaying item details and handling Stripe payments.

Main Views:
    - buy_view: Creates a Stripe Checkout session and returns the session ID.
    - item_view: Renders a product detail page with Stripe publishable key.
    - success_view: Simple HTML response for successful payment.
    - cancel_view: Simple HTML response for canceled payment.

Dependencies:
    - Stripe API for payment integration
    - Django shortcuts and HTTP utilities for request handling and rendering
    - Local Item model
"""

import stripe
from django.conf import settings
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_view(request, item_id):
    """
    Initiates a Stripe Checkout session for the specified item.

    :param request: Django HttpRequest object (must be GET).
    :param item_id: ID of the item to purchase.
    :return: JSON response containing the Stripe Checkout session ID.
    :raises Http404: If the request method is not GET or item does not exist.
    """
    if request.method != 'GET':
        raise Http404()

    item = get_object_or_404(Item, pk=item_id)

    domain = request.build_absolute_uri('/')[:-1]
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency.lower(),
                    'unit_amount': int(item.price * 100),   # cents
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'id': checkout_session.id})


def item_view(request, item_id):
    """
    Renders a product detail page with the Stripe publishable key.

    :param request: Django HttpRequest object.
    :param item_id: ID of the item to display.
    :return: Rendered HTML page with item details.
    :raises Http404: If the item is not found.
    """
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'item': item,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'store/single_item.html', context)


def success_view(request):
    """
    Returns a simple HTML page indicating a successful payment.

    :param request: Django HttpRequest object.
    :return: HttpResponse with success message.
    """
    return HttpResponse("<html><body><h1>Payment successful!</h1>"
                        "<p>Thank you for your purchase.</p></body></html>")


def cancel_view(request):
    """
    Returns a simple HTML page indicating a canceled payment.

    :param request: Django HttpRequest object.
    :return: HttpResponse with cancellation message.
    """
    return HttpResponse("<html><body><h1>Payment canceled.</h1>"
                        "<p>Your payment was not completed.</p></body></html>")


def order_detail_view(request, order_id):
    """
    GET /store/order/<order_id>/
    Renders the page showing details of the Order and Payment Element.
    """
    order = get_object_or_404(Order, pk=order_id)

    context = {
        'order': order,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }

    return render(request, 'store/order_detail.html', context)


def create_checkout_session(request, order_id):
    """
    Creates a Stripe Checkout session for the given order and returns JSON response with session ID.

    :param request: Django HttpRequest object.
    :param order_id: ID of the order to create checkout session for.
    :return: JsonResponse containing Stripe session ID on success, or error message on failure.
    """
    order = get_object_or_404(Order, pk=order_id)

    line_items = []
    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'unit_amount': int(item.price * 100),
                'product_data': {
                    'name': item.name,
                },
            },
            'quantity': 1,
        })

    # Create a Stripe TaxRate if a tax is applied
    tax_rate = None
    if order.tax and order.tax.percentage > 0:
        tax_rate = stripe.TaxRate.create(
            display_name=order.tax.name or "Tax",
            inclusive=False,
            percentage=order.tax.percentage,
            country="US",  # you can specify your own country code
        )

    # Add tax rate to each item
    if tax_rate:
        for item in line_items:
            item["tax_rates"] = [tax_rate.id]

    # Create a coupon if a discount is applied
    coupon = None
    if order.discount and order.discount.percentage > 0:
        coupon = stripe.Coupon.create(
            percent_off=order.discount.percentage,
            duration='once',
        )
        discount = {'coupon': coupon.id}
        discounts = [discount]
    else:
        discounts = []

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
            discounts=discounts,
        )
        return JsonResponse({'session_id': session.id})
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)
