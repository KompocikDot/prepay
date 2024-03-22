from django.urls import path

from users.views import AddAdditionalAccountDataView

urlpatterns = [
    path(
        "additional-data/",
        AddAdditionalAccountDataView.as_view(),
        name="add_additional_account_data",
    ),
]
