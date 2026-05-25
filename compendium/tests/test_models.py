import io
import pytest
from PIL import Image
from django.core.files.base import ContentFile

from compendium.models import Skill, DevilFruit, Monster, Scenario, Subscriber


def make_image():
    buf = io.BytesIO()
    Image.new("RGB", (1, 1)).save(buf, format="PNG")
    buf.seek(0)
    return ContentFile(buf.read())


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username="test",
        email="test@example.com",
        password="pass123",
    )


@pytest.fixture
def skill(db, user):
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
        name="Mera Mera no Mi",
        fruit_type="Logia",
        description="Fire fruit.",
        author=user,
    )
    fruit.image.save("mera.png", make_image(), save=False)
    fruit.save()
    fruit.skills.add(skill)
    return fruit


@pytest.fixture
def monster(db, user, skill):
    monster_instance = Monster(
        name="Sea King",
        description="Giant sea creature.",
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
    monster_instance.image.save("sea_king.png", make_image(), save=False)
    monster_instance.save()
    monster_instance.skills.add(skill)
    return monster_instance


@pytest.fixture
def scenario(db, user, monster):
    scenario_instance = Scenario.objects.create(
        title="The Grand Line Crossing",
        description="Cross the Grand Line.",
        starting_hook="A map appears.",
        author=user,
    )
    scenario_instance.monsters.add(monster)
    return scenario_instance


@pytest.fixture
def subscriber(db):
    return Subscriber.objects.create(email="sub@example.com")


def test_user_str(user):
    assert str(user) == "test"


def test_subscriber_str(subscriber):
    assert str(subscriber) == "sub@example.com"


def test_skill_str(skill):
    assert str(skill) == "Gomu Gomu no Pistol: 2d6, Attack"


def test_skill_slug_is_auto_generated(skill):
    assert skill.slug == "gomu-gomu-no-pistol"


def test_skill_slug_is_not_overwritten_on_update(skill):
    skill.name = "New Name"
    skill.save()
    assert skill.slug == "gomu-gomu-no-pistol"


def test_devil_fruit_str(devil_fruit):
    assert str(devil_fruit) == "Mera Mera no Mi: Logia"


def test_devil_fruit_slug_is_auto_generated(devil_fruit):
    assert devil_fruit.slug == "mera-mera-no-mi"


def test_monster_str(monster):
    assert str(monster) == "Sea King"


def test_monster_slug_is_auto_generated(monster):
    assert monster.slug == "sea-king"


def test_scenario_str(scenario):
    assert str(scenario) == "The Grand Line Crossing"


def test_scenario_slug_is_auto_generated(scenario):
    assert scenario.slug == "the-grand-line-crossing"


def test_scenario_slug_is_not_overwritten_on_update(scenario):
    scenario.title = "New Title"
    scenario.save()
    assert scenario.slug == "the-grand-line-crossing"