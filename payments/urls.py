from django.urls import path

from .views import (
    PaymentPostView,
    PaymentsCreateView,
    PaymentsDetailView,
    PaymentsListView,
    PaymentsQRView,
    PaymentStripeView,
)

urlpatterns = [
    path("payments/", PaymentsListView.as_view(), name="payments_list"),
    path("payment/", PaymentsCreateView.as_view(), name="create_payment"),
    path("payments/<int:pk>/qr/", PaymentsQRView.as_view(), name="payment_qr"),
    path("payments/<int:pk>/", PaymentsDetailView.as_view(), name="payment_details"),
    path(
        "payments/<int:pk>/complete/",
        PaymentStripeView.as_view(),
        name="complete_payment",
    ),
    path(
        "payments/<int:pk>/after/",
        PaymentPostView.as_view(),
        name="post_payment",
    ),
]
