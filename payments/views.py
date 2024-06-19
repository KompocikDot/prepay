import os
from io import BytesIO
from typing import Any

from django.db import models
import qrcode
import qrcode.image.svg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView
from stripe import PaymentIntent

from payments.stripe import StripePayment

from .forms import CreatePaymentForm
from .models import Payment


def generate_qr_code(url: str) -> str:
    qr_code = qrcode.QRCode(image_factory=qrcode.image.svg.SvgPathImage)
    qr_code.add_data(url)
    qr_code.make(fit=True)
    qr_img = qr_code.make_image(attrib={"class": "fill-cyan-500 h-full w-full"})
    svg = BytesIO()
    qr_img.save(stream=svg)

    return svg.getvalue().decode()


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
        return reverse_lazy(
            "payment_details", kwargs={"pk": getattr(self.object, "id")}
        )


class PaymentsDetailView(LoginRequiredMixin, DetailView):
    model = Payment

    def get_queryset(self) -> models.query.QuerySet[Payment]:
        return Payment.objects.filter(issuer=self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        if self.object.status == Payment.PaymentStatus.CREATED:
            payment_url = reverse_lazy(
                "payment_qr", kwargs={"pk": self.kwargs.get("pk")}
            )
            ctx["qr_svg"] = generate_qr_code(payment_url)
        return ctx


class PaymentsQRView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment_qr.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        payment_url = reverse_lazy("payment_qr", kwargs={"pk": self.kwargs.get("pk")})
        ctx["qr_svg"] = generate_qr_code(payment_url)
        return ctx


class PaymentStripeView(LoginRequiredMixin, DetailView):
    template_name = "payments/stripe_payment.html"
    model = Payment

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        user_id: int | None = request.user.id

        if self.object.issuer.id == user_id:
            # redirect if user is issuer of payment
            return HttpResponse(
                "Your not allowed to complete your own payment", status=403
            )

        payment_intent = self.create_payment_intent()
        self.assign_intent_to_model(payment_intent)

        context = self.get_context_data(object=self.object, user=request.user)
        context["payment_client_secret"] = payment_intent.client_secret

        return self.render_to_response(context)

    def assign_intent_to_model(self, stripe_payment: PaymentIntent) -> None:
        self.object.stripe_payment_id = stripe_payment.id
        self.object.save()

    def create_payment_intent(self) -> PaymentIntent:
        app_fee = os.getenv("APP_FEE")
        if not app_fee:
            raise Exception("APP FEE CANNOT BE EMPTY")

        payment = self.object
        return StripePayment(
            name=payment.name,
            amount=int(payment.amount.amount * 100),  # FIX: temporary fix
            currency=payment.amount.currency,
            app_fee=int(app_fee),
            payer_id=self.request.user.id,
        ).create_intent(payment.issuer.stripe_account_id)


class PaymentPostView(LoginRequiredMixin, TemplateView):
    template_name = "payments/post_payment.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        client_secret = self.request.GET.get("payment_intent")
        redirect_status = self.request.GET.get("redirect_status")
        if client_secret and StripePayment.is_intent_successfully_completed(
            client_secret
        ):

            return super().get(request, *args, **kwargs)
        return HttpResponse(f"Bad stripe status: {redirect_status}", status=400)


class PaymentAwaitStatusView(LoginRequiredMixin, DetailView):
    template_name = "payments/partial/status.html"
