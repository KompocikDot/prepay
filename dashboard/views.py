import logging
from typing import Any

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from payments.models import Payment


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "./dashboard/dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.request.user
        issued_payments_count = Payment.objects.filter(issuer=user).count()
        last_five_end_user_payments = Payment.objects.filter(end_user=user).order_by(
            "-id"
        )[:5]

        end_user_payments_count = Payment.objects.filter(end_user=user).count()

        ctx = {
            "issued_payments_count": issued_payments_count,
            "last_five_end_user_payments": last_five_end_user_payments,
            "end_user_payments_count": end_user_payments_count,
        }

        self.get_stripe_balance()
        return ctx

    def get_stripe_balance(self):
        balance = stripe.Balance.retrieve(
            stripe_account=self.request.user.stripe_account_id
        )

        logging.error(balance)
