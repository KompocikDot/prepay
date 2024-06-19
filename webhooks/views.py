import logging
import os

import stripe
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from payments.models import Payment
from users.models import User


@method_decorator(csrf_exempt, name="dispatch")
class StripePaymentWebhook(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not secret:
            return HttpResponse(status=500)

        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(request.body, sig_header, secret)
        except stripe.error.SignatureVerificationError as e:
            print("Webhook signature verification failed. " + str(e))
            return HttpResponse(status=500)

        if event and event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]  # contains a stripe.PaymentIntent
            try:
                payment = Payment.objects.get(stripe_payment_id=payment_intent.id)
                payment.status = Payment.PaymentStatus.CONFIRMED
                logging.exception(payment_intent)
                payment.end_user = User.objects.get(
                    id=payment_intent["metadata"]["user_id"]
                )
                payment.save()

            except Payment.DoesNotExist:
                print(f"Payment with: {payment_intent.id} does not exsits")
                return HttpResponse(status=500)
            # Then define and call a method to handle the successful payment intent.
            # handle_payment_intent_succeeded(payment_intent)

        return HttpResponse(status=200)
