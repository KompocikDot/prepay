import os
from io import BytesIO
from typing import Any

import qrcode
import qrcode.image.svg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView

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

    def form_valid(self, form: CreatePaymentForm) -> HttpResponse:
        form.instance.issuer = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("payment_view", kwargs={"pk": self.object.get("id")})


class PaymentsDetailView(LoginRequiredMixin, DetailView):
    model = Payment


class PaymentsQRView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment_qr.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        payment_url = reverse_lazy("payment_qr", kwargs={"pk": self.kwargs.get("pk")})
        ctx["qr_svg"] = self.generate_qr_code(payment_url)
        return ctx

    @staticmethod
    def generate_qr_code(url: str) -> str:
        qr_code = qrcode.make(data=url, image_factory=qrcode.image.svg.SvgPathImage)
        svg = BytesIO()
        qr_code.save(stream=svg)

        return svg.getvalue().decode()


class PaymentStripeView(LoginRequiredMixin, DetailView):
    template_name = "payments/stripe_payment.html"
    model = Payment

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        user_id: int | None = request.user.id

        if self.object.issuer.id == user_id:
            # redirect if user is issuer of payment
            return self.render_to_response({})
        context = self.get_context_data(object=self.object, user=request.user)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)

        payment: Payment = ctx["payment"]
        app_fee = os.getenv("APP_FEE")
        if not app_fee:
            raise Exception("APP FEE CANNOT BE EMPTY")

        ctx["payment_client_secret"] = StripePayment(
            name=payment.name,
            amount=int(payment.amount.amount * 100),  # temporary fix
            currency=payment.amount.currency,
            app_fee=int(app_fee),
        ).create_intent(payment.issuer.stripe_account_id)

        return ctx


class PaymentSubmitView(LoginRequiredMixin, DetailView):
    template_name = "payments/stripe_post_submit.html"
    model = Payment  # TODO: Think how it should work, what's expected outcome and changes to payment model etc.
