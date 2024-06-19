from django.urls import path

from users.views import AddAdditionalAccountDataView, UserProfileView

urlpatterns = [
    path(
        "additional-data/",
        AddAdditionalAccountDataView.as_view(),
        name="additional_account_data",
    ),
    path("", UserProfileView.as_view(), name="profile"),
]
