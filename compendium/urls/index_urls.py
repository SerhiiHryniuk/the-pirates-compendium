from django.urls import path

from compendium.views import IndexView, RegisterView
from compendium.views.subscribe_views import SubscribeView

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
    ),
    path(
        "subscribe/",
        SubscribeView.as_view(),
        name='subscribe'
    ),
]
