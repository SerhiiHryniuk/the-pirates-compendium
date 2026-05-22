from django.urls import path

from compendium.views import IndexView, RegisterView

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name='index'
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name='register'
    )
]
