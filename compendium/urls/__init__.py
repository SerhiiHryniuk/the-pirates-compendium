from compendium.urls import index_urls, skills_urls, devil_fruits_urls, monsters_urls, scenarios_urls

app_name = "compendium"

urlpatterns = (
    index_urls.urlpatterns
    + skills_urls.urlpatterns
    + devil_fruits_urls.urlpatterns
    + monsters_urls.urlpatterns
    + scenarios_urls.urlpatterns
)