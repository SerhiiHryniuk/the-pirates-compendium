import io
import pytest
from PIL import Image
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from compendium.models import Monster


def make_image_file():
    buf = io.BytesIO()
    Image.new("RGB", (1, 1), color="red").save(buf, format="PNG")
    buf.seek(0)
    return SimpleUploadedFile(
        "test.png",
        buf.read(),
        content_type="image/png"
    )


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
def skill(db, user):
    from compendium.models import Skill
    return Skill.objects.create(
        name="Bite",
        description="A bite attack.",
        dmg_dice="1d6",
        skill_type="Attack",
        author=user,
    )


@pytest.fixture
def monster(db, user, skill):
    m = Monster(
        name="Sea King",
        description="A giant sea creature.",
        origin="Grand Line",
        health_points=120,
        armor_class=15,
        challenge_rating=8,
        speed=30,
        strength=20,
        dexterity=8,
        constitution=18,
        intelligence=4,
        wisdom=6,
        charisma=5,
        author=user,
    )
    m.image.save(
        "sea_king.png",
        ContentFile(make_image_file().read()),
        save=False
    )
    m.save()
    m.skills.add(skill)
    return m


def form_data(skill):
    return {
        "name": "Kraken",
        "description": "A giant squid.",
        "origin": "Deep Sea",
        "health_points": 200,
        "armor_class": 18,
        "challenge_rating": 12,
        "speed": 20,
        "strength": 25,
        "dexterity": 5,
        "constitution": 22,
        "intelligence": 3,
        "wisdom": 5,
        "charisma": 2,
        "skills": [skill.pk],
    }


def test_monster_detail_increments_view_count(
        client,
        monster
):
    client.get(reverse(
        "compendium:monster_detail",
        kwargs={"slug": monster.slug})
    )
    monster.refresh_from_db()
    assert monster.view_count == 1


def test_monster_create_logged_in_user_can_create(
        client,
        user,
        skill
):
    client.force_login(user)
    response = client.post(
        reverse(
            "compendium:monster_create"
        ),
        {
            **form_data(skill),
            "image": make_image_file()
        },
    )
    assert response.status_code == 302


def test_monster_create_author_is_set(
        client,
        user,
        skill
):
    client.force_login(user)
    client.post(
        reverse(
            "compendium:monster_create"
        ),
        {
            **form_data(skill),
            "image": make_image_file()
        },
    )
    assert Monster.objects.get(name="Kraken").author == user


def test_monster_update_owner_can_update(
        client,
        user,
        monster,
        skill
):
    client.force_login(user)
    client.post(
        reverse(
            "compendium:monster_update",
            kwargs={"slug": monster.slug}
        ),
        {
            **form_data(skill),
            "name": "Updated Sea King",
            "image": make_image_file()
        },
    )
    monster.refresh_from_db()
    assert monster.name == "Updated Sea King"


def test_monster_update_non_owner_is_forbidden(
        client,
        other_user,
        monster,
        skill
):
    client.force_login(other_user)
    response = client.post(
        reverse(
            "compendium:monster_update",
            kwargs={"slug": monster.slug}
        ),
        {
            **form_data(skill),
            "name": "Updated Sea King",
            "image": make_image_file()
        },
    )
    assert response.status_code == 403


def test_monster_delete_owner_can_delete(
        client,
        user,
        monster
):
    client.force_login(user)
    client.post(reverse(
        "compendium:monster_delete",
        kwargs={"slug": monster.slug})
    )
    assert not Monster.objects.filter(pk=monster.pk).exists()


def test_monster_delete_non_owner_cannot_delete(
        client,
        other_user,
        monster
):
    client.force_login(other_user)
    client.post(reverse(
        "compendium:monster_delete",
        kwargs={"slug": monster.slug})
    )
    assert Monster.objects.filter(pk=monster.pk).exists()
