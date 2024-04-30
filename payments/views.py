import os
from io import BytesIO
from typing import Any

import qrcode
import qrcode.image.svg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from djmoney.models.fields import MoneyField

from payments.stripe import StripePayment

from .forms import CreatePaymentForm
from .models import Payment


class PaymentsListView(LoginRequiredMixin, ListView):
    model = Payment
    paginate_by = 50

    def get_queryset(self) -> QuerySet[Payment]:
        return Payment.objects.filter(issuer__id=self.request.user.pk).order_by(
            "-created_at"
        )


class PaymentsCreateView(LoginRequiredMixin, CreateView):
    template_name = "payments/create_payment.html"
    form_class = CreatePaymentForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form: CreatePaymentForm) -> HttpResponse:
        form.instance.issuer = self.request.user
        return super().form_valid(form)


class PaymentsDetailView(LoginRequiredMixin, DetailView):
    model = Payment


class PaymentsQRView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment_qr.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        payment_url = ""
        ctx["qr_svg"] = self.generate_qr_code(payment_url)
        return ctx

    @staticmethod
    def generate_qr_code(url: str) -> str:
        qr_code = qrcode.make(data=url, image_factory=qrcode.image.svg.SvgPathImage)
        svg = BytesIO()
        qr_code.save(stream=svg)

        return svg.getvalue().decode()


class PaymentStripeView(DetailView):
    template_name = "payments/stripe_payment.html"
    model = Payment

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        payment: Payment = ctx["payment"]
        app_fee = os.getenv("APP_FEE")
        if not app_fee:
            raise Exception("APP FEE CANNOT BE EMPTY")

        ctx["stripe_client_secret"] = StripePayment(
            name=payment.name,
            amount=int(payment.amount.amount * 100),
            currency=payment.amount.currency,
            app_fee=int(app_fee),
        ).create_intent(payment.issuer.stripe_account_id)

        return ctx
