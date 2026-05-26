import io
import pytest
from django.core import mail
from django.urls import reverse
from django.core.files.base import ContentFile
from PIL import Image

from compendium.models import Scenario


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username="test",
        email="test@example.com",
        password="pass123",
    )


@pytest.fixture
def other_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username="other",
        email="other@example.com",
        password="pass123",
    )


@pytest.fixture
def monster(db, user):
    from compendium.models import Monster

    def make_image():
        buf = io.BytesIO()
        Image.new("RGB", (1, 1), color="red").save(buf, format="PNG")
        buf.seek(0)
        return ContentFile(buf.read())

    m = Monster(
        name="Sea King",
        description="A giant sea creature.",
        origin="Grand Line",
        health_points=100,
        armor_class=14,
        challenge_rating=6,
        speed=30,
        strength=18,
        dexterity=8,
        constitution=16,
        intelligence=4,
        wisdom=6,
        charisma=4,
        author=user,
    )
    m.image.save("sea_king.png", make_image(), save=False)
    m.save()
    return m


@pytest.fixture
def scenario(db, user, monster):
    s = Scenario.objects.create(
        title="The Grand Line Crossing",
        description="The crew must cross the Grand Line.",
        starting_hook="A map leads the crew to the Grand Line.",
        author=user,
    )
    s.monsters.add(monster)
    return s


def form_data(monster):
    return {
        "title": "Arlong Park Siege",
        "description": "Storm Arlong's base.",
        "starting_hook": "Nami asks the crew for help.",
        "monsters": [monster.pk],
    }


def test_scenario_detail_increments_view_count(
        client,
        scenario
):
    client.get(reverse(
        "compendium:scenario_detail",
        kwargs={"slug": scenario.slug})
    )
    scenario.refresh_from_db()
    assert scenario.view_count == 1


def test_scenario_create_logged_in_user_can_create(
        client,
        user,
        monster
):
    client.force_login(user)
    response = client.post(reverse(
        "compendium:scenario_create"
    ),
        form_data(monster)
    )
    assert response.status_code == 302


def test_scenario_create_author_is_set(
        client,
        user,
        monster
):
    client.force_login(user)
    client.post(reverse(
        "compendium:scenario_create"
    ),
        form_data(monster)
    )
    assert Scenario.objects.get(title="Arlong Park Siege").author == user


def test_scenario_create_notifies_subscribers(
        client,
        user,
        monster
):
    from compendium.models import Subscriber
    Subscriber.objects.create(email="sub1@test.com")
    Subscriber.objects.create(email="sub2@test.com")

    client.force_login(user)
    client.post(reverse(
        "compendium:scenario_create"
    ),
        form_data(monster)
    )

    assert "Arlong Park Siege" in mail.outbox[0].subject


def test_scenario_create_no_email_when_no_subscribers(
        client,
        user,
        monster
):
    client.force_login(user)
    client.post(reverse(
        "compendium:scenario_create"
    ),
        form_data(monster)
    )
    assert len(mail.outbox) == 0


def test_scenario_update_owner_can_update(
        client,
        user,
        scenario,
        monster
):
    client.force_login(user)
    client.post(
        reverse(
            "compendium:scenario_update",
            kwargs={"slug": scenario.slug}
        ),
        {
            **form_data(monster),
            "title": "Updated Scenario"
        },
    )
    scenario.refresh_from_db()
    assert scenario.title == "Updated Scenario"


def test_scenario_update_non_owner_is_forbidden(
        client,
        other_user,
        scenario,
        monster
):
    client.force_login(other_user)
    response = client.post(
        reverse(
            "compendium:scenario_update",
            kwargs={"slug": scenario.slug}
        ),
        {
            **form_data(monster),
            "title": "Updated Scenario"
        },
    )
    assert response.status_code == 403


def test_scenario_delete_owner_can_delete(
        client,
        user,
        scenario
):
    client.force_login(user)
    client.post(reverse(
        "compendium:scenario_delete",
        kwargs={"slug": scenario.slug})
    )
    assert not Scenario.objects.filter(pk=scenario.pk).exists()


def test_scenario_delete_non_owner_cannot_delete(
        client,
        other_user,
        scenario
):
    client.force_login(other_user)
    client.post(reverse(
        "compendium:scenario_delete",
        kwargs={"slug": scenario.slug})
    )
    assert Scenario.objects.filter(pk=scenario.pk).exists()
