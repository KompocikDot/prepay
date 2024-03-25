from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

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
