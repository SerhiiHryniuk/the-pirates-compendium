import pytest
from django.urls import reverse

from compendium.models import Skill


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
        name="Gomu Gomu no Pistol",
        description="A rubber punch.",
        dmg_dice="2d6",
        skill_type="Attack",
        author=user,
    )


def test_skill_detail_increments_view_count(client, skill):
    client.get(reverse("compendium:skill_detail", kwargs={"slug": skill.slug}))
    skill.refresh_from_db()
    assert skill.view_count == 1


def test_skill_create_logged_in_user_can_create(client, user):
    client.force_login(user)
    response = client.post(reverse("compendium:skill_create"), {
        "name": "Haki Burst",
        "description": "An armament burst.",
        "dmg_dice": "1d8",
        "skill_type": "Attack",
    })
    assert response.status_code == 302


def test_skill_create_author_is_set(client, user):
    client.force_login(user)
    client.post(reverse("compendium:skill_create"), {
        "name": "Haki Burst",
        "description": "An armament burst.",
        "dmg_dice": "1d8",
        "skill_type": "Attack",
    })
    assert Skill.objects.get(name="Haki Burst").author == user


def test_skill_update_owner_can_update(client, user, skill):
    client.force_login(user)
    client.post(
        reverse(
            "compendium:skill_update",
            kwargs={"slug": skill.slug}
        ),
        {
            "name": "Updated",
            "description": "Updated",
            "dmg_dice": "3d6",
            "skill_type": "Attack"
        },
    )
    skill.refresh_from_db()
    assert skill.name == "Updated"


def test_skill_update_non_owner_is_forbidden(client, other_user, skill):
    client.force_login(other_user)
    response = client.post(
        reverse(
            "compendium:skill_update",
            kwargs={"slug": skill.slug}
        ),
        {
            "name": "Updated",
            "description": "Updated",
            "dmg_dice": "1d4",
            "skill_type": "Attack"
        },
    )
    assert response.status_code == 403


def test_skill_delete_owner_can_delete(client, user, skill):
    client.force_login(user)
    client.post(reverse(
        "compendium:skill_delete",
        kwargs={"slug": skill.slug})
    )
    assert not Skill.objects.filter(pk=skill.pk).exists()


def test_skill_delete_non_owner_cannot_delete(client, other_user, skill):
    client.force_login(other_user)
    client.post(reverse(
        "compendium:skill_delete",
        kwargs={"slug": skill.slug})
    )
    assert Skill.objects.filter(pk=skill.pk).exists()
