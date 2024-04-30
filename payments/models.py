
from django.db import IntegrityError, models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator

from .utils import gen_external_id
from users.models import User


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        CREATED = "CREATED"
        WAITING_FOR_STRIPE_CONFIRMATION = "WAITING_FOR_STRIPE_CONFIRMATION"
        CONFIRMED = "CONFIRMED"

    status = models.CharField(
        choices=PaymentStatus.choices, default=PaymentStatus.CREATED
    )

    name = models.CharField(max_length=255)
    issuer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="issuer")
    end_user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="end_user",
    )

    amount = MoneyField(
        max_digits=7,
        decimal_places=2,
        currency_choices=[("USD", "USD $"), ("EUR", "EUR €"), ("PLN", "PLN zł")],
        validators=[
            MinMoneyValidator({"EUR": 1, "PLN": 5, "USD": 1}),
            MaxMoneyValidator({"EUR": 20000, "PLN": 99999, "USD": 20000}),
        ],
    )

    external_id = models.CharField(default=gen_external_id)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.issuer.username} | {self.external_id} | {self.amount}"

    def save(self, *args, **kwargs) -> None:
        while True:
            try:
                saved = super().save(*args, **kwargs)
                return saved
            except IntegrityError:
                pass


