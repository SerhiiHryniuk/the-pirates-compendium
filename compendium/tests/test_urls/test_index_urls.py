from django.urls import (
    reverse,
    resolve
)

from compendium.views import (
    IndexView,
    RegisterView
)
from compendium.views.subscribe_views import SubscribeView


def test_index_url():
    assert resolve(
        reverse("compendium:index")
    ).func.view_class == IndexView


def test_register_url():
    assert resolve(
        reverse("compendium:register")
    ).func.view_class == RegisterView


def test_subscribe_url():
    assert resolve(
        reverse("compendium:subscribe")
    ).func.view_class == SubscribeView
