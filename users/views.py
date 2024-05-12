from datetime import date
from logging import log

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.edit import FormView

from payments.stripe import StripeAccount
from users.forms import AddAdditionalDataForm, UserProfileForm
from users.models import User


class AddAdditionalAccountDataView(LoginRequiredMixin, FormView):
    form_class = AddAdditionalDataForm
    template_name = "additional_data/add_account_data.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None) -> User:
        return User.objects.get(pk=self.request.user.id)  # type: ignore

    def get_form(self, *args, **kwargs):
        if self.request.method in ["POST", "PUT"]:
            return AddAdditionalDataForm(self.request.POST, instance=self.get_object())
        return AddAdditionalDataForm(instance=self.get_object())

    def form_valid(self, form: AddAdditionalDataForm) -> HttpResponse:
        filled = self.get_object().additional_data_filled_in
        if not filled:
            instance: User = form.instance
            account = StripeAccount(
                first_name=instance.first_name,
                last_name=instance.last_name,
                email=instance.email,
                birth_date=date(2003, 1, 16),
                phone_number=instance.phone_number,
                address="Wrocław",
            )

            account_id = account.create()
            instance.stripe_account_id = account_id
            form.save()

        return super(AddAdditionalAccountDataView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.get_object().additional_data_filled_in:
            return redirect("profile")
        return super().get(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, CreateView):
    form_class = UserProfileForm
    template_name = "profile/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, *args, **kwargs) -> User:
        return User.objects.get(pk=self.request.user.id)  # type: ignore

    def get_form(self, *args, **kwargs):
        if self.request.method in ["POST", "PUT"]:
            return UserProfileForm(self.request.POST, instance=self.get_object())
        return UserProfileForm(instance=self.get_object())
