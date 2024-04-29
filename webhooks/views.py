import os
from django.http import HttpRequest, HttpResponse
from django.views import View
import stripe

class StripePaymentWebhook(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        secret = os.getenv("STRIPE_ENDPOINT_SECRET")
        if not secret:
            return HttpResponse(status_code=500)

        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        if not sig_header:
            return HttpResponse(status_code=400)
        try:
            event = stripe.Webhook.construct_event(
                request.POST, sig_header, secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('Webhook signature verification failed.' + str(e))
            return HttpResponse(status_code=500) 

        return HttpResponse(status_code=200)

