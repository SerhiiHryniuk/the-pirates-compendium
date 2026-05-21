from django.urls import path

from compendium.views import IndexView

urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name='index'
    ),
]
