import logging
import os
from datetime import datetime
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
        birth_date: datetime,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.birth_date = birth_date

    def create(self) -> None:
        try:
            account = stripe.Account.create(type="express")
            self.id = account.id
        except Exception as e:
            log(logging.ERROR, e)

    def link(self, refresh_url: str, return_url: str) -> None:
        if not self.id:
            raise NoStripeAccountIDException

        stripe.AccountLink.create(
            account=self.id,
            refresh_url=refresh_url,
            return_url=return_url,
            type="account_onboarding",
        )


class StripePayment:
    def __init__(self, name: str, amount: int, currency: str, app_fee: int) -> None:
        self.name = name
        self.amount = amount
        self.currency = currency
        self.app_fee = app_fee

    def create_session(
        self, success_url: str, cancel_url: str, account_id: str
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
                "transfer_data": {"destination": account_id},
            },
            success_url=success_url,
            cancel_url=cancel_url,
        )

    def create_intent(self, issuer_uuid: str) -> str:
        intent = stripe.PaymentIntent.create(
            amount=self.amount,
            currency=self.currency,
            automatic_payment_methods={"enabled": True},
            application_fee_amount=self.app_fee,
            transfer_data={"destination": issuer_uuid},
        )

        secret = intent.client_secret
        if not secret:
            raise NoStripeClientSecretException

        return secret
