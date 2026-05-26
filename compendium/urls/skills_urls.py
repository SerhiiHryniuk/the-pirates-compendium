from django.urls import path

from compendium.views import (
    SkillListView,
    SkillSearchView,
    SkillCreateView,
    SkillDetailView,
    SkillUpdateView,
    SkillDeleteView,
    SkillPdfView
)

urlpatterns = [
    path(
        "skills/",
        SkillListView.as_view(),
        name="skill_list"
    ),
    path(
        "skills/search/",
        SkillSearchView.as_view(),
        name="skill_search"
    ),
    path(
        "skills/create/",
        SkillCreateView.as_view(),
        name="skill_create"
    ),
    path(
        "skills/<slug:slug>/",
        SkillDetailView.as_view(),
        name="skill_detail"
    ),
    path(
        "skills/<slug:slug>/update/",
        SkillUpdateView.as_view(),
        name="skill_update"
    ),
    path(
        "skills/<slug:slug>/delete/",
        SkillDeleteView.as_view(),
        name="skill_delete"
    ),
    path(
        "skills/<slug:slug>/pdf/",
        SkillPdfView.as_view(),
        name="skill_pdf"
    ),
]
