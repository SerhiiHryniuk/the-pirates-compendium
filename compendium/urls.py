from django.urls import path

from compendium.views import IndexView, SkillListView

app_name = "compendium"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("skills/", SkillListView.as_view(), name="skill_list"),
]