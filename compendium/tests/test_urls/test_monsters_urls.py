from django.urls import (
    reverse,
    resolve
)

from compendium.views import (
    MonsterListView,
    MonsterSearchView,
    MonsterCreateView,
    MonsterDetailView,
    MonsterUpdateView,
    MonsterDeleteView,
    MonsterPdfView,
)


def test_monster_list_url():
    assert resolve(
        reverse("compendium:monster_list")
    ).func.view_class == MonsterListView


def test_monster_search_url():
    assert resolve(
        reverse("compendium:monster_search")
    ).func.view_class == MonsterSearchView


def test_monster_create_url():
    assert resolve(
        reverse("compendium:monster_create")
    ).func.view_class == MonsterCreateView


def test_monster_detail_url():
    assert resolve(
        reverse("compendium:monster_detail",
                kwargs={"slug": "test-monster"})
    ).func.view_class == MonsterDetailView


def test_monster_update_url():
    assert resolve(
        reverse("compendium:monster_update",
                kwargs={"slug": "test-monster"})
    ).func.view_class == MonsterUpdateView


def test_monster_delete_url():
    assert resolve(
        reverse("compendium:monster_delete",
                kwargs={"slug": "test-monster"})
    ).func.view_class == MonsterDeleteView


def test_monster_pdf_url():
    assert resolve(
        reverse("compendium:monster_pdf",
                kwargs={"slug": "test-monster"})
    ).func.view_class == MonsterPdfView
