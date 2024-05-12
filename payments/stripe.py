import logging
import os
from datetime import date, datetime, timezone
from logging import log

import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")


class NoStripeAccountIDException(Exception):
    pass


class NoStripeClientSecretException(Exception):
    pass


class StripeAccount:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
        address: str,
        birth_date: date,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.birth_date = birth_date

    def create(self) -> str | None:
        try:
            account = stripe.Account.create(
                type="custom",
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
                business_type="individual",
                individual={
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "dob": {
                        "year": self.birth_date.year,
                        "month": self.birth_date.month,
                        "day": self.birth_date.day,
                    },
                    "address": {
                        "line1": self.address,
                        "postal_code": "15-349",  # FIXME: Change it later on
                        "city": "Białystok",
                    },
                    "email": self.email,
                    "phone": self.phone_number,
                },
                tos_acceptance={
                    "ip": "127.0.0.1",  # FIXME: Change it later on to pass it from request
                    "date": int(datetime.strftime(datetime.now(timezone.utc), "%s")),
                },
                business_profile={
                    "mcc": "4829",
                    "url": "https://soczko.com/",
                },
            )

            return account.id

        except Exception as e:
            log(logging.ERROR, e)


class StripePayment:
    def __init__(self, name: str, amount: int, currency: str, app_fee: int) -> None:
        self.name = name
        self.amount = amount
        self.currency = currency
        self.app_fee = app_fee

    def create_session(
        self, success_url: str, cancel_url: str, issuer_uuid: str
    ) -> None:
        stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "quantity": 1,
                    "price_data": {
                        "currency": self.currency,
                        "product_data": {
                            "name": self.name,
                        },
                        "unit_amount": self.amount,
                    },
                },
            ],
            payment_intent_data={
                "application_fee_amount": self.app_fee,
                "transfer_data": {"destination": issuer_uuid},
            },
            success_url=success_url,
            cancel_url=cancel_url,
        )

    def create_intent(self, issuer_uuid: str) -> str:
        intent = stripe.PaymentIntent.create(
            amount=self.amount,
            currency=self.currency,
            payment_method_types=[
                "card",
                "p24",
            ],
            application_fee_amount=self.app_fee,
            transfer_data={"destination": issuer_uuid},
        )

        secret = intent.client_secret
        if not secret:
            raise NoStripeClientSecretException

        return secret
