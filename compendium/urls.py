from django.urls import path

from compendium.views import IndexView, SkillListView, SkillCreateView, SkillDetailView, SkillUpdateView, \
    SkillDeleteView, DevilFruitListView

app_name = "compendium"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("skills/", SkillListView.as_view(), name="skill_list"),
    path("skills/<slug:slug>/", SkillDetailView.as_view(), name="skill_detail"),
    path("skills/create/", SkillCreateView.as_view(), name="skill_create"),
    path("skills/<slug:slug>/update/", SkillUpdateView.as_view(), name="skill_update"),
    path("skills/<slug:slug>/delete/", SkillDeleteView.as_view(), name="skill_delete"),
    path("devil-fruit/", DevilFruitListView.as_view(), name="devil_fruit_list")
]