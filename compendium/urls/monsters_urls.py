from django.urls import path

from compendium.views import (
    MonsterListView,
    MonsterSearchView,
    MonsterCreateView,
    MonsterDetailView,
    MonsterUpdateView,
    MonsterDeleteView,
    MonsterPdfView
)

urlpatterns = [
    path(
        "monster/",
        MonsterListView.as_view(),
        name="monster_list"
    ),
    path(
        "monster/search/",
        MonsterSearchView.as_view(),
        name="monster_search"
    ),
    path(
        "monster/create/",
        MonsterCreateView.as_view(),
        name="monster_create"
    ),
    path(
        "monster/<slug:slug>/",
        MonsterDetailView.as_view(),
        name="monster_detail"
    ),
    path(
        "monster/<slug:slug>/update/",
        MonsterUpdateView.as_view(),
        name="monster_update"
    ),
    path(
        "monster/<slug:slug>/delete/",
        MonsterDeleteView.as_view(),
        name="monster_delete"
    ),
    path(
        "monster/<slug:slug>/pdf/",
        MonsterPdfView.as_view(),
        name="monster_pdf"
    ),
]
