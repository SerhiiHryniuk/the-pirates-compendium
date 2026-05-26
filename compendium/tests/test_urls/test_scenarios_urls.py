from django.urls import (
    reverse,
    resolve
)

from compendium.views import (
    ScenarioListView,
    ScenarioSearchView,
    ScenarioCreateView,
    ScenarioDetailView,
    ScenarioUpdateView,
    ScenarioDeleteView,
    ScenarioPdfView,
)


def test_scenario_list_url():
    assert resolve(
        reverse("compendium:scenario_list")
    ).func.view_class == ScenarioListView


def test_scenario_search_url():
    assert resolve(
        reverse("compendium:scenario_search")
    ).func.view_class == ScenarioSearchView


def test_scenario_create_url():
    assert resolve(
        reverse("compendium:scenario_create")
    ).func.view_class == ScenarioCreateView


def test_scenario_detail_url():
    assert resolve(
        reverse("compendium:scenario_detail",
                kwargs={"slug": "test-scenario"})
    ).func.view_class == ScenarioDetailView


def test_scenario_update_url():
    assert resolve(
        reverse("compendium:scenario_update",
                kwargs={"slug": "test-scenario"})
    ).func.view_class == ScenarioUpdateView


def test_scenario_delete_url():
    assert resolve(
        reverse("compendium:scenario_delete",
                kwargs={"slug": "test-scenario"})
    ).func.view_class == ScenarioDeleteView


def test_scenario_pdf_url():
    assert resolve(
        reverse("compendium:scenario_pdf",
                kwargs={"slug": "test-scenario"})
    ).func.view_class == ScenarioPdfView
