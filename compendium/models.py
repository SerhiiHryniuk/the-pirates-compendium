from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class SkillType(models.TextChoices):
    ATTACK = "Attack"
    PASSIVE = "Passive"
    SPECIAl = "Special"


class DevilFruitType(models.TextChoices):
    LOGIA = "Logia"
    PARAMECIA = "Paramecia"
    ZOAN = "Zoan"


class User(AbstractUser):
    pass


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)


class Skill(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    dmg_dice = models.CharField(max_length=63, blank=True)
    skill_type = models.CharField(
        max_length=10,
        choices=SkillType.choices
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.dmg_dice}, {self.skill_type}, {self.description[:25]}..."


class DevilFruit(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    fruit_type = models.CharField(
        max_length=10,
        choices=DevilFruitType.choices
    )
    description = models.TextField()
    image = models.ImageField(upload_to='images/devil_fruits/')
    view_count = models.PositiveIntegerField(default=0)
    skills = models.ManyToManyField(Skill, related_name="devil_fruits")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devil_fruits")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.fruit_type}, {self.description[:25]}..."


class Monster(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.description[:25]}..."

class Scenario(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    starting_hook = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    monsters = models.ManyToManyField(Monster, related_name="scenarios")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scenarios")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}: {self.description[:25]}..."
