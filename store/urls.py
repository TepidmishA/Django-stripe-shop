"""
URL Configuration Module

Defines URL patterns for the 'store' app, mapping paths to view functions.
"""

from django.urls import path

from . import views

app_name = 'store'  # for namespace "store"

urlpatterns = [
    path('item/<int:item_id>/', views.item_view, name='item'),
    path('buy/<int:item_id>/', views.buy_view, name='buy'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='canceled'),

    path("order/<int:order_id>/", views.order_detail_view, name="order_detail"),
    path("order/<int:order_id>/create-checkout-session/", views.create_checkout_session,
         name="create_checkout_session"),
]
