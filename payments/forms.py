from django.forms.models import ModelForm

from payments.models import Payment


class CreatePaymentForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["amount"].widget.widgets[0].attrs.update(
            {
                "class": "block w-full rounded-l-md border-0 py-1.5 pl-2 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            }
        )

        self.fields["amount"].widget.widgets[1].attrs.update(
            {
                "class": "block rounded-r-md border-0 py-1.5 pl-2 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            }
        )
        self.fields["name"].widget.attrs.update(
            {
                "class": "block w-full rounded-md border-0 py-1.5 pl-2 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            }
        )

    class Meta:
        model = Payment
        fields = ["amount", "name"]
