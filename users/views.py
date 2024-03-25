from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

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
            form.save()
        return super(AddAdditionalAccountDataView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.get_object().additional_data_filled_in:
            return redirect("profile")
        return super().get(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, FormView):
    form_class = UserProfileForm
    template_name = "profile/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None) -> User:
        return User.objects.get(pk=self.request.user.id)  # type: ignore

    def get_form(self, *args, **kwargs):
        if self.request.method in ["POST", "PUT"]:
            return UserProfileForm(self.request.POST, instance=self.get_object())
        return UserProfileForm(instance=self.get_object())

    def form_valid(self, form: UserProfileForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)
