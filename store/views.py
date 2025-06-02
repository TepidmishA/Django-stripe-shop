import stripe
from django.conf import settings
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_view(request, item_id):
    """
    GET /buy/<item_id>/
    """
    # Filter to only GET requests
    if request.method != 'GET':
        raise Http404()

    item = get_object_or_404(Item, pk=item_id)

    # Create line_items for Stripe
    domain = request.build_absolute_uri('/')[:-1]
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(item.price * 100),
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
    GET /item/<item_id>/
    """
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'item': item,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'store/single_item.html', context)


def success_view(request):
    return HttpResponse("<html><body><h1>Payment successful!</h1><p>Thank you for your purchase.</p></body></html>")


def cancel_view(request):
    return HttpResponse("<html><body><h1>Payment canceled.</h1><p>Your payment was not completed.</p></body></html>")
