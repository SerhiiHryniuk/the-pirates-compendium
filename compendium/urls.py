from django.urls import path

from compendium.views import index


app_name = "compendium"

urlpatterns = [
    path("", index, name="index"),
]