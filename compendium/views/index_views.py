from django.views.generic import TemplateView

from compendium.models import (
    Skill,
    DevilFruit,
    Monster,
    Scenario
)


class IndexView(TemplateView):
    template_name = 'compendium/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill_count'] = Skill.objects.count()
        context['devil_fruit_count'] = DevilFruit.objects.count()
        context['monster_count'] = Monster.objects.count()
        context['scenario_count'] = Scenario.objects.count()
        context['top_skills'] = Skill.objects.order_by(
            '-view_count',
            'name'
        )[:3]
        context['top_devil_fruits'] = DevilFruit.objects.order_by(
            '-view_count',
            'name'
        )[:3]
        context['top_monsters'] = Monster.objects.order_by(
            '-view_count',
            'name'
        )[:3]
        context['top_scenarios'] = Scenario.objects.order_by(
            '-view_count',
            'title'
        )[:3]
        return context
