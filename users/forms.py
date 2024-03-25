from django.forms.models import ModelForm

from .models import User


class AddAdditionalDataForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddAdditionalDataForm, self).__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ["phone_number", "first_name", "last_name"]
        required = ["phone_number", "first_name", "last_name"]


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].required = True

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "phone_number"]
