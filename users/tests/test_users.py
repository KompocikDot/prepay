from django.test import TestCase
from django.urls import reverse

from users.models import User


class TestUsers(TestCase):
    ACCOUNT_URL = reverse("additional_account_data")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="test_user", email="test@test.com", password="Test1234!"
        )

    def login_user(self) -> None:
        logged = self.client.login(username=self.user.username, password="Test1234!")
        self.assertTrue(logged)

    def test_get_additional_data_form_not_logged(self) -> None:
        res = self.client.get(self.ACCOUNT_URL, follow=True)
        self.assertRedirects(
            res,
            reverse("account_login") + f"?next={self.ACCOUNT_URL}",
        )

    def test_get_additional_data_form_without_data_set(self) -> None:
        self.login_user()
        res = self.client.get(self.ACCOUNT_URL)
        self.assertEqual(res.status_code, 200)

    def test_add_addtional_data(self) -> None:
        self.login_user()
        res = self.client.post(
            self.ACCOUNT_URL,
            data={
                "phone_number": "+48123123123",
                "first_name": "testuser_first_name",
                "last_name": "testuser_last_name",
            },
        )
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, "testuser_first_name")
        self.assertEqual(updated_user.last_name, "testuser_last_name")
        self.assertEqual(updated_user.phone_number, "+48123123123")
        self.assertRedirects(res, reverse("profile"))

    def test_get_additional_data_form_with_data_set(self) -> None:
        self.login_user()
        self.client.post(
            self.ACCOUNT_URL,
            data={
                "phone_number": "+48123123123",
                "first_name": "testuser_first_name",
                "last_name": "testuser_last_name",
            },
        )

        res = self.client.get(self.ACCOUNT_URL)
        self.assertRedirects(res, reverse("profile"))
