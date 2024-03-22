from django.contrib.auth.models import AbstractUser, models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)

    @property
    def additional_data_filled(self):
        return (
            self.first_name != "" and self.last_name != "" and self.phone_number != ""
        )
