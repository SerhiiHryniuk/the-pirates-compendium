from django.urls import (
    reverse,
    resolve
)

from compendium.views import (
    DevilFruitListView,
    DevilFruitSearchView,
    DevilFruitCreateView,
    DevilFruitDetailView,
    DevilFruitUpdateView,
    DevilFruitDeleteView,
    DevilFruitPdfView,
)


def test_devil_fruit_list_url():
    assert resolve(
        reverse("compendium:devil_fruit_list")
    ).func.view_class == DevilFruitListView


def test_devil_fruit_search_url():
    assert resolve(
        reverse("compendium:devil_fruit_search")
    ).func.view_class == DevilFruitSearchView


def test_devil_fruit_create_url():
    assert resolve(
        reverse("compendium:devil_fruit_create")
    ).func.view_class == DevilFruitCreateView


def test_devil_fruit_detail_url():
    assert resolve(
        reverse("compendium:devil_fruit_detail",
                kwargs={"slug": "test-fruit"})
    ).func.view_class == DevilFruitDetailView


def test_devil_fruit_update_url():
    assert resolve(
        reverse("compendium:devil_fruit_update",
                kwargs={"slug": "test-fruit"})
    ).func.view_class == DevilFruitUpdateView


def test_devil_fruit_delete_url():
    assert resolve(
        reverse("compendium:devil_fruit_delete",
                kwargs={"slug": "test-fruit"})
    ).func.view_class == DevilFruitDeleteView


def test_devil_fruit_pdf_url():
    assert resolve(
        reverse("compendium:devil_fruit_pdf",
                kwargs={"slug": "test-fruit"})
    ).func.view_class == DevilFruitPdfView
