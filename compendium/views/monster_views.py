from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from weasyprint import HTML

from compendium.models import Monster, Skill


@method_decorator(never_cache, name='dispatch')
class MonsterListView(ListView):
    model = Monster
    template_name = 'compendium/monsters_templates/monster_list.html'
    context_object_name = 'monster_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_monsters'] = Monster.objects.order_by('-view_count', 'name')[:3]
        return context


class MonsterSearchView(ListView):
    model = Monster
    template_name = 'compendium/monsters_templates/monster_search_results.html'
    context_object_name = 'monster_list'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            return Monster.objects.filter(name__icontains=query)
        return Monster.objects.all()


class MonsterCreateView(LoginRequiredMixin, CreateView):
    model = Monster
    fields = ['name', 'description', 'origin', 'image', 'health_points', 'armor_class', 'challenge_rating', 'speed', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'skills']
    template_name = 'compendium/monsters_templates/monster_form.html'
    success_url = reverse_lazy('compendium:monster_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class MonsterDetailView(DetailView):
    model = Monster
    template_name = 'compendium/monsters_templates/monster_detail.html'
    context_object_name = 'monster_detail'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count = F('view_count') + 1
        obj.save(update_fields=['view_count'])
        obj.refresh_from_db()
        return obj


class MonsterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Monster
    fields = ['name', 'description', 'origin', 'image', 'health_points', 'armor_class', 'challenge_rating', 'speed', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'skills']
    template_name = 'compendium/monsters_templates/monster_form.html'
    success_url = reverse_lazy('compendium:monster_list')

    def test_func(self):
        monster = self.get_object()
        return self.request.user == monster.author

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form


class MonsterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Monster
    template_name = 'compendium/monsters_templates/monster_delete.html'
    success_url = reverse_lazy('compendium:monster_list')

    def test_func(self):
        monster = self.get_object()
        return self.request.user == monster.author


class MonsterPdfView(DetailView):
    model = Monster

    def render_to_response(self, context, **response_kwargs):
        monster = self.object
        image_path = monster.image.path.replace('\\', '/') if monster.image else None
        html_content = render_to_string('compendium/monsters_templates/monster_pdf.html', {'monster': monster, 'image_path': image_path})
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="monster_{monster.slug}.pdf"'
        return response
