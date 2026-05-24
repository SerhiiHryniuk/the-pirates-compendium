from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from weasyprint import HTML

from compendium.models import Skill


class SkillListView(ListView):
    model = Skill
    template_name = 'compendium/skills_templates/skill_list.html'
    context_object_name = 'skill_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_skills'] = Skill.objects.order_by(
            '-view_count',
            'name'
        )[:3]
        return context


class SkillSearchView(ListView):
    model = Skill
    template_name = 'compendium/skills_templates/skill_search_results.html'
    context_object_name = 'skill_list'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            return Skill.objects.filter(name__icontains=query)
        return Skill.objects.all()


class SkillDetailView(DetailView):
    model = Skill
    template_name = 'compendium/skills_templates/skill_detail.html'
    context_object_name = 'skill_detail'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count = F('view_count') + 1
        obj.save(update_fields=['view_count'])
        obj.refresh_from_db()
        return obj


class SkillCreateView(LoginRequiredMixin, CreateView):
    model = Skill
    fields = ['name', 'description', 'dmg_dice', 'skill_type']
    template_name = 'compendium/skills_templates/skill_form.html'
    success_url = reverse_lazy('compendium:skill_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SkillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Skill
    fields = ['name', 'description', 'dmg_dice', 'skill_type']
    template_name = 'compendium/skills_templates/skill_form.html'
    success_url = reverse_lazy('compendium:skill_list')

    def test_func(self):
        skill = self.get_object()
        return self.request.user == skill.author


class SkillDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Skill
    template_name = 'compendium/skills_templates/skill_delete.html'
    success_url = reverse_lazy('compendium:skill_list')

    def test_func(self):
        skill = self.get_object()
        return self.request.user == skill.author


class SkillPdfView(DetailView):
    model = Skill

    def render_to_response(self, context, **response_kwargs):
        skill = self.object
        html_content = render_to_string('compendium/skills_templates/skill_pdf.html', {'skill': skill})
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="skill_{skill.slug}.pdf"'
        return response
