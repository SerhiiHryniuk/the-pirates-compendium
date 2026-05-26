import io
import pytest
from PIL import Image
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

from compendium.models import DevilFruit


def make_image_file():
    buf = io.BytesIO()
    Image.new("RGB", (1, 1), color="red").save(buf, format="PNG")
    buf.seek(0)
    return SimpleUploadedFile("test.png", buf.read(), content_type="image/png")


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


@pytest.fixture
def devil_fruit(db, user, skill):
    fruit = DevilFruit(
        name="Gomu Gomu no Mi",
        fruit_type="Paramecia",
        description="Turns the user into rubber.",
        author=user,
    )
    fruit.image.save(
        "gomu.png",
        ContentFile(make_image_file().read()),
        save=False
    )
    fruit.save()
    fruit.skills.add(skill)
    return fruit


def form_data(skill):
    return {
        "name": "Mera Mera no Mi",
        "fruit_type": "Logia",
        "description": "Turns the user into fire.",
        "skills": [skill.pk],
    }


def test_devil_fruit_detail_increments_view_count(
        client,
        devil_fruit
):
    client.get(reverse(
        "compendium:devil_fruit_detail",
        kwargs={"slug": devil_fruit.slug})
    )
    devil_fruit.refresh_from_db()
    assert devil_fruit.view_count == 1


def test_devil_fruit_create_logged_in_user_can_create(
        client,
        user,
        skill
):
    client.force_login(user)
    response = client.post(
        reverse(
            "compendium:devil_fruit_create"
        ),
        {
            **form_data(skill),
            "image": make_image_file()
        },
    )
    assert response.status_code == 302


def test_devil_fruit_create_author_is_set(
        client,
        user,
        skill
):
    client.force_login(user)
    client.post(
        reverse(
            "compendium:devil_fruit_create"
        ),
        {
            **form_data(skill),
            "image": make_image_file()
        },
    )
    assert DevilFruit.objects.get(name="Mera Mera no Mi").author == user


def test_devil_fruit_update_owner_can_update(
        client,
        user,
        devil_fruit,
        skill
):
    client.force_login(user)
    client.post(
        reverse(
            "compendium:devil_fruit_update",
            kwargs={"slug": devil_fruit.slug}
        ),
        {
            **form_data(skill),
            "name": "Updated Fruit",
            "image": make_image_file()
        },
    )
    devil_fruit.refresh_from_db()
    assert devil_fruit.name == "Updated Fruit"


def test_devil_fruit_update_non_owner_is_forbidden(
        client,
        other_user,
        devil_fruit,
        skill
):
    client.force_login(other_user)
    response = client.post(
        reverse(
            "compendium:devil_fruit_update",
            kwargs={"slug": devil_fruit.slug}
        ),
        {
            **form_data(skill),
            "name": "Updated Fruit",
            "image": make_image_file()
        },
    )
    assert response.status_code == 403


def test_devil_fruit_delete_owner_can_delete(
        client,
        user,
        devil_fruit
):
    client.force_login(user)
    client.post(reverse(
        "compendium:devil_fruit_delete",
        kwargs={"slug": devil_fruit.slug})
    )
    assert not DevilFruit.objects.filter(pk=devil_fruit.pk).exists()


def test_devil_fruit_delete_non_owner_cannot_delete(
        client,
        other_user,
        devil_fruit
):
    client.force_login(other_user)
    client.post(reverse(
        "compendium:devil_fruit_delete",
        kwargs={"slug": devil_fruit.slug})
    )
    assert DevilFruit.objects.filter(pk=devil_fruit.pk).exists()
