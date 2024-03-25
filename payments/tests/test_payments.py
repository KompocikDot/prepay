from django.test.testcases import TestCase
from django.urls import reverse


class TestPayments(TestCase):
    PAYMENTS_LIST_URL = reverse("payments_list")
    LOGIN_URL = reverse("account_login")
    PAYMENTS_CREATE_URL = reverse("payments_create")

    def test_get_payments_list_unauthorized(self) -> None:
        res = self.client.get(self.PAYMENTS_LIST_URL)
        self.assertRedirects(res, self.LOGIN_URL + f"?next={self.PAYMENTS_LIST_URL}")

    def test_get_create_payment_unauthorized(self) -> None:
        res = self.client.get(self.PAYMENTS_CREATE_URL)
        self.assertRedirects(res, self.LOGIN_URL + f"?next={self.PAYMENTS_CREATE_URL}")

    def test_get_create_payment(self) -> None:
        pass
