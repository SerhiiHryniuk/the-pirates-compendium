from django import forms
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from compendium.models import Skill, DevilFruit, Monster


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


class SkillUpdateView(UpdateView):
    model = Skill
    fields = ['name', 'slug', 'description', 'dmg_dice', 'skill_type']
    template_name = 'compendium/skill_form.html'
    success_url = reverse_lazy('compendium:skill_list')


class SkillDeleteView(DeleteView):
    model = Skill
    template_name = 'compendium/skill_delete.html'
    success_url = reverse_lazy('compendium:skill_list')


class DevilFruitListView(ListView):
    model = DevilFruit
    template_name = 'compendium/devil_fruit_list.html'
    context_object_name = 'devil_fruit_list'


class DevilFruitCreateView(CreateView):
    model = DevilFruit
    fields = ['name', 'slug', 'fruit_type', 'description', 'image', 'skills']
    template_name = 'compendium/devil_fruit_form.html'
    success_url = reverse_lazy('compendium:devil_fruit_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DevilFruitDetailView(DetailView):
    model = DevilFruit
    template_name = 'compendium/devil_fruit_detail.html'
    context_object_name = 'devil_fruit_detail'


class DevilFruitUpdateView(UpdateView):
    model = DevilFruit
    fields = ['name', 'slug', 'fruit_type', 'description', 'image', 'skills']
    template_name = 'compendium/devil_fruit_form.html'
    success_url = reverse_lazy('compendium:devil_fruit_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form


class DevilFruitDeleteView(DeleteView):
    model = DevilFruit
    template_name = 'compendium/devil_fruit_delete.html'
    success_url = reverse_lazy('compendium:devil_fruit_list')


class MonsterListView(ListView):
    model = Monster
    template_name = 'compendium/monster_list.html'
    context_object_name = 'monster_list'


class MonsterCreateView(CreateView):
    model = Monster
    fields = ['name', 'slug', 'description', 'origin', 'image', 'health_points', 'armor_class', 'challenge_rating', 'speed', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'skills']
    template_name = 'compendium/monster_form.html'
    success_url = reverse_lazy('compendium:monster_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class MonsterDetailView(DetailView):
    model = Monster
    template_name = 'compendium/monster_detail.html'
    context_object_name = 'monster_detail'