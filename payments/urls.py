from django.urls import path

from .views import PaymentsCreateView, PaymentsListView

urlpatterns = [
    path("payments/", PaymentsListView.as_view(), name="payments_list"),
    path("payment/", PaymentsCreateView.as_view(), name="create_payment"),
]
