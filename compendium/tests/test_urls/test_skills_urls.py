from django.urls import (
    reverse,
    resolve
)

from compendium.views import (
    SkillListView,
    SkillSearchView,
    SkillCreateView,
    SkillDetailView,
    SkillUpdateView,
    SkillDeleteView,
    SkillPdfView,
)


def test_skill_list_url():
    assert resolve(
        reverse("compendium:skill_list")
    ).func.view_class == SkillListView


def test_skill_search_url():
    assert resolve(
        reverse("compendium:skill_search")
    ).func.view_class == SkillSearchView


def test_skill_create_url():
    assert resolve(
        reverse("compendium:skill_create")
    ).func.view_class == SkillCreateView


def test_skill_detail_url():
    assert resolve(
        reverse("compendium:skill_detail",
                kwargs={"slug": "test-skill"})
    ).func.view_class == SkillDetailView


def test_skill_update_url():
    assert resolve(
        reverse("compendium:skill_update",
                kwargs={"slug": "test-skill"})
    ).func.view_class == SkillUpdateView


def test_skill_delete_url():
    assert resolve(
        reverse("compendium:skill_delete",
                kwargs={"slug": "test-skill"})
    ).func.view_class == SkillDeleteView


def test_skill_pdf_url():
    assert resolve(
        reverse("compendium:skill_pdf",
                kwargs={"slug": "test-skill"})
    ).func.view_class == SkillPdfView
