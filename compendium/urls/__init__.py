from compendium.urls import index, skills, devil_fruits, monsters, scenarios

app_name = "compendium"

urlpatterns = (
        index
        + skills
        + devil_fruits
        + monsters
        + scenarios
)
