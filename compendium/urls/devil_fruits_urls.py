from django.urls import path

from compendium.views import (
    DevilFruitListView,
    DevilFruitSearchView,
    DevilFruitCreateView,
    DevilFruitDetailView,
    DevilFruitUpdateView,
    DevilFruitDeleteView,
    DevilFruitPdfView
)

urlpatterns = [
    path(
        "devil-fruit/",
        DevilFruitListView.as_view(),
        name="devil_fruit_list"
    ),
    path(
        "devil-fruit/search/",
        DevilFruitSearchView.as_view(),
        name="devil_fruit_search"
    ),
    path(
        "devil-fruit/create/",
        DevilFruitCreateView.as_view(),
        name="devil_fruit_create"
    ),
    path(
        "devil-fruit/<slug:slug>/",
        DevilFruitDetailView.as_view(),
        name="devil_fruit_detail"
    ),
    path(
        "devil-fruit/<slug:slug>/update/",
        DevilFruitUpdateView.as_view(),
        name="devil_fruit_update"
    ),
    path(
        "devil-fruit/<slug:slug>/delete/",
        DevilFruitDeleteView.as_view(),
        name="devil_fruit_delete"
    ),
    path(
        "devil-fruit/<slug:slug>/pdf/",
        DevilFruitPdfView.as_view(),
        name="devil_fruit_pdf"
    ),
]
