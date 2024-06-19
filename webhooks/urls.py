from django.urls import path

from webhooks.views import StripePaymentWebhook

urlpatterns = [
    path("stripe/", StripePaymentWebhook.as_view(), name="stripe_webhook"),
]
