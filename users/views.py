from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from users.forms import AddAdditionalDataForm
from users.models import User


class AddAdditionalAccountDataView(LoginRequiredMixin, FormView):
    form_class = AddAdditionalDataForm
    template_name = "add_additional_account_data.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def get_form(self, *args, **kwargs):
        if self.request.method in ["POST", "PUT"]:
            return AddAdditionalDataForm(self.request.POST, instance=self.get_object())
        return AddAdditionalDataForm(instance=self.get_object())

    def form_valid(self, form: AddAdditionalDataForm):
        if not self.get_object().additional_data_filled:
            form.save()
        return super(AddAdditionalAccountDataView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.get_object().additional_data_filled:
            return redirect("profile")
        return super().get(request, *args, **kwargs)
