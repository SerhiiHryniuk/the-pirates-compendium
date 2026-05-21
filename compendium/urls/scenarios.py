from django.urls import path

from compendium.views import (
    ScenarioListView,
    ScenarioSearchView,
    ScenarioCreateView,
    ScenarioDetailView,
    ScenarioUpdateView,
    ScenarioDeleteView,
    ScenarioPdfView
)

urlpatterns = [
    path(
        "scenario/",
        ScenarioListView.as_view(),
        name="scenario_list"
    ),
    path(
        "scenario/search/",
        ScenarioSearchView.as_view(),
        name="scenario_search"
    ),
    path(
        "scenario/create/",
        ScenarioCreateView.as_view(),
        name="scenario_create"
    ),
    path(
        "scenario/<slug:slug>/",
        ScenarioDetailView.as_view(),
        name="scenario_detail"
    ),
    path(
        "scenario/<slug:slug>/update/",
        ScenarioUpdateView.as_view(),
        name="scenario_update"
    ),
    path(
        "scenario/<slug:slug>/delete/",
        ScenarioDeleteView.as_view(),
        name="scenario_delete"
    ),
    path(
        "scenario/<slug:slug>/pdf/",
        ScenarioPdfView.as_view(),
        name="scenario_pdf"
    ),
]
