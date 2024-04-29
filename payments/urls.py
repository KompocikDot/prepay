from django.urls import path

from .views import PaymentsCreateView, PaymentsListView, PaymentsQRView

urlpatterns = [
    path("payments/", PaymentsListView.as_view(), name="payments_list"),
    path("payment/", PaymentsCreateView.as_view(), name="create_payment"),
    path("payment/<str:external_id>", PaymentsQRView.as_view(), name="payment_qr"),
]
