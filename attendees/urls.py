

from django.urls import path
from .views import payment_callback, paystack_webhook, register, register_success

urlpatterns = [
    path('register/', register, name='register'),
    path('payment/callback/', payment_callback, name='payment_callback'),
    path('payment/webhook/', paystack_webhook, name='paystack_webhook'),
    path('register/success/', register_success, name='register_success'),
]
