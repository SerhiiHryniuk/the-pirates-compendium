from django.views.generic import TemplateView, ListView

from compendium.models import Skill


class IndexView(TemplateView):
    template_name = 'compendium/index.html'


class SkillListView(ListView):
    model = Skill
    template_name = 'compendium/skill_list.html'
    context_object_name = 'skill_list'

