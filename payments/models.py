from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator

from users.models import User


class Payment(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.issuer.username} | {self.pk} | {self.amount}"
