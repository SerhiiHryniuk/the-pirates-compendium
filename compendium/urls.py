from django.urls import path

from compendium.views import IndexView, SkillListView, SkillCreateView, SkillDetailView, SkillUpdateView, \
    SkillDeleteView, DevilFruitListView, DevilFruitCreateView, DevilFruitDetailView, DevilFruitUpdateView, \
    DevilFruitDeleteView, MonsterListView, MonsterCreateView, MonsterDetailView, MonsterUpdateView, MonsterDeleteView, \
    ScenarioListView, ScenarioCreateView, ScenarioUpdateView, ScenarioDetailView, ScenarioDeleteView, SkillPdfView, \
    DevilFruitPdfView, MonsterPdfView, ScenarioPdfView, SkillSearchView

app_name = "compendium"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("skills/", SkillListView.as_view(), name="skill_list"),
    path("skills/search/", SkillSearchView.as_view(), name="skill_search"),
    path("skills/create/", SkillCreateView.as_view(), name="skill_create"),
    path("skills/<slug:slug>/", SkillDetailView.as_view(), name="skill_detail"),
    path("skills/<slug:slug>/update/", SkillUpdateView.as_view(), name="skill_update"),
    path("skills/<slug:slug>/delete/", SkillDeleteView.as_view(), name="skill_delete"),
    path("skills/<slug:slug>/pdf/", SkillPdfView.as_view(), name="skill_pdf"),
    path("devil-fruit/", DevilFruitListView.as_view(), name="devil_fruit_list"),
    path("devil-fruit/create/", DevilFruitCreateView.as_view(), name="devil_fruit_create"),
    path("devil-fruit/<slug:slug>/", DevilFruitDetailView.as_view(), name="devil_fruit_detail"),
    path("devil-fruit/<slug:slug>/update/", DevilFruitUpdateView.as_view(), name="devil_fruit_update"),
    path("devil-fruit/<slug:slug>/delete/", DevilFruitDeleteView.as_view(), name="devil_fruit_delete"),
    path("devil-fruit/<slug:slug>/pdf/", DevilFruitPdfView.as_view(), name="devil_fruit_pdf"),
    path("monster/", MonsterListView.as_view(), name="monster_list"),
    path("monster/create/", MonsterCreateView.as_view(), name="monster_create"),
    path("monster/<slug:slug>/", MonsterDetailView.as_view(), name="monster_detail"),
    path("monster/<slug:slug>/update/", MonsterUpdateView.as_view(), name="monster_update"),
    path("monster/<slug:slug>/delete/", MonsterDeleteView.as_view(), name="monster_delete"),
    path("monster/<slug:slug>/pdf/", MonsterPdfView.as_view(), name="monster_pdf"),
    path("scenario/", ScenarioListView.as_view(), name="scenario_list"),
    path("scenario/create/", ScenarioCreateView.as_view(), name="scenario_create"),
    path("scenario/<slug:slug>/", ScenarioDetailView.as_view(), name="scenario_detail"),
    path("scenario/<slug:slug>/update/", ScenarioUpdateView.as_view(), name="scenario_update"),
    path("scenario/<slug:slug>/delete/", ScenarioDeleteView.as_view(), name="scenario_delete"),
    path("scenario/<slug:slug>/pdf/", ScenarioPdfView.as_view(), name="scenario_pdf"),
]