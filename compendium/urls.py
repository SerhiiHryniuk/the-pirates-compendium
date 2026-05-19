from django.urls import path

from compendium.views import IndexView

app_name = "compendium"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]