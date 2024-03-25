from django.test.testcases import TestCase
from django.urls import reverse, reverse_lazy

from payments.models import Payment
from users.models import User


class TestPayments(TestCase):
    PAYMENTS_LIST_URL = reverse("payments_list")
    LOGIN_URL = reverse("account_login")
    PAYMENTS_CREATE_URL = reverse("create_payment")
    PROFILE_URL = reverse("profile")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="test_user", email="test@test.com", password="Test1234!"
        )

    def login_user(self) -> None:
        logged = self.client.login(username=self.user.username, password="Test1234!")
        self.assertTrue(logged)

    def test_get_payments_list_unauthorized(self) -> None:
        res = self.client.get(self.PAYMENTS_LIST_URL, follow=True)
        self.assertRedirects(res, self.LOGIN_URL + f"?next={self.PAYMENTS_LIST_URL}")

    def test_get_create_payment_unauthorized(self) -> None:
        res = self.client.get(self.PAYMENTS_CREATE_URL, follow=True)
        self.assertRedirects(res, self.LOGIN_URL + f"?next={self.PAYMENTS_CREATE_URL}")

    def test_get_create_payment(self) -> None:
        self.login_user()
        res = self.client.get(self.PAYMENTS_CREATE_URL)
        self.assertEqual(res.status_code, 200)

    def test_create_payment(self) -> None:
        self.login_user()
        res = self.client.post(
            self.PAYMENTS_CREATE_URL, data={"amount_0": "5", "amount_1": "USD"}
        )
        # FIX: Change redirect URL to something other later on
        self.assertRedirects(res, self.PROFILE_URL)
        self.assertTrue(Payment.objects.filter(issuer__id=self.user.pk).exists())

    # TODO: Add tests for forms
