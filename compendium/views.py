from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from compendium.models import Skill


class IndexView(TemplateView):
    template_name = 'compendium/index.html'


class SkillListView(ListView):
    model = Skill
    template_name = 'compendium/skill_list.html'
    context_object_name = 'skill_list'


class SkillDetailView(DetailView):
    model = Skill
    template_name = 'compendium/skill_detail.html'
    context_object_name = 'skill_detail'


class SkillCreateView(CreateView):
    model = Skill
    fields = ['name', 'slug', 'description', 'dmg_dice', 'skill_type']
    template_name = 'compendium/skill_form.html'
    success_url = reverse_lazy('compendium:skill_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

