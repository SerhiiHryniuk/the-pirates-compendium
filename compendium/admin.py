from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from compendium.models import (
    Subscriber,
    DevilFruit,
    Monster,
    Scenario,
    Skill
)

admin.site.register(User, UserAdmin)
admin.site.register(Subscriber)
admin.site.register(Skill)
admin.site.register(DevilFruit)
admin.site.register(Monster)
admin.site.register(Scenario)
