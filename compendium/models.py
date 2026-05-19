from django.contrib.auth.models import AbstractUser
from django.db import models


class SkillType(models.TextChoices):
    ATTACK = "Attack",
    PASSIVE = "Passive",
    SPECIAl = "Special"


class DevilFruitType(models.TextChoices):
    LOGIA = "Logia",
    PARAMECIA = "Paramecia",
    ZOAN = "Zoan"


class User(AbstractUser):
    pass


class Subscriber(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)


class Skill(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    dmg_dice = models.CharField(max_length=63)
    skill_type = models.CharField(
        max_length=10,
        choices=SkillType.choices
    )


class DevilFruit(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    fruit_type = models.CharField(
        max_length=10,
        choices=DevilFruitType.choices
    )
    description = models.TextField()
    image = models.ImageField(upload_to='images/devil_fruits/')
    view_count = models.PositiveIntegerField(default=0)
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="devil_fruits")


class Monster(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    origin = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/monsters/')
    health_points = models.PositiveIntegerField(default=1)
    armor_class = models.PositiveIntegerField(default=1)
    challenge_rating = models.PositiveIntegerField(default=0)
    speed = models.PositiveIntegerField(default=0)
    strength = models.PositiveIntegerField(default=0)
    dexterity = models.PositiveIntegerField(default=0)
    constitution = models.PositiveIntegerField(default=0)
    intelligence = models.PositiveIntegerField(default=0)
    wisdom = models.PositiveIntegerField(default=0)
    charisma = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="monsters")
    skills = models.ManyToManyField(Skill, related_name="monsters")


class Scenario(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    starting_hook = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    monsters = models.ManyToManyField(Monster, related_name="scenarios")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scenarios")
