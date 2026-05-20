from django import forms
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from weasyprint import HTML

from compendium.models import Skill, DevilFruit, Monster, Scenario


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
    fields = ['name', 'description', 'dmg_dice', 'skill_type']
    template_name = 'compendium/skill_form.html'
    success_url = reverse_lazy('compendium:skill_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SkillUpdateView(UpdateView):
    model = Skill
    fields = ['name', 'description', 'dmg_dice', 'skill_type']
    template_name = 'compendium/skill_form.html'
    success_url = reverse_lazy('compendium:skill_list')


class SkillDeleteView(DeleteView):
    model = Skill
    template_name = 'compendium/skill_delete.html'
    success_url = reverse_lazy('compendium:skill_list')


class SkillPdfView(DetailView):
    model = Skill

    def render_to_response(self, context, **response_kwargs):
        skill = self.object
        html_content = f"""
                <html>
                <body>
                    <h1>Skill: {skill.name}</h1>
                    <p><strong>Damage:</strong> {skill.dmg_dice}</p>
                    <p><strong>Type:</strong> {skill.skill_type}</p>
                    <p><strong>Description:</strong> {skill.description}</p>
                    <p><strong>Author:</strong> {skill.author.username}</p>
                </body>
                </html>
                """
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="skill_{skill.slug}.pdf"'
        return response


class DevilFruitListView(ListView):
    model = DevilFruit
    template_name = 'compendium/devil_fruit_list.html'
    context_object_name = 'devil_fruit_list'


class DevilFruitCreateView(CreateView):
    model = DevilFruit
    fields = ['name', 'fruit_type', 'description', 'image', 'skills']
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
    fields = ['name', 'fruit_type', 'description', 'image', 'skills']
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


class DevilFruitPdfView(DetailView):
    model = DevilFruit

    def render_to_response(self, context, **response_kwargs):
        fruit = self.object
        image_html = ""
        if fruit.image:
            clean_path = fruit.image.path.replace('\\', '/')
            image_html = f'<img src="file:///{clean_path}" style="max-width: 250px; height: auto; display: block; margin: 10px 0;">'
        skills_html = "".join([f"<li>{skill.name}</li>" for skill in fruit.skills.all()])
        html_content = f"""
        <html>
        <body>
            <h1>{fruit.name}</h1>
            <p>Type: {fruit.fruit_type}</p>
            <p>Description: {fruit.description}</p>

            {image_html}

            <h3>Skills:</h3>
            <ul>
                {skills_html}
            </ul>
        </body>
        </html>
        """
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="skill_{fruit.slug}.pdf"'
        return response


class MonsterListView(ListView):
    model = Monster
    template_name = 'compendium/monster_list.html'
    context_object_name = 'monster_list'


class MonsterCreateView(CreateView):
    model = Monster
    fields = ['name', 'description', 'origin', 'image', 'health_points', 'armor_class', 'challenge_rating', 'speed', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'skills']
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


class MonsterUpdateView(UpdateView):
    model = Monster
    fields = ['name', 'description', 'origin', 'image', 'health_points', 'armor_class', 'challenge_rating', 'speed', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'skills']
    template_name = 'compendium/monster_form.html'
    success_url = reverse_lazy('compendium:monster_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form


class MonsterDeleteView(DeleteView):
    model = Monster
    template_name = 'compendium/monster_delete.html'
    success_url = reverse_lazy('compendium:monster_list')


class MonsterPdfView(DetailView):
    model = Monster

    def render_to_response(self, context, **response_kwargs):
        monster = self.object
        image_html = ""
        if monster.image:
            clean_path = monster.image.path.replace('\\', '/')
            image_html = f'<img src="file:///{clean_path}" style="max-width: 250px; height: auto; display: block; margin: 10px 0;">'
        skills_html = "".join([f"<li>{skill.name}</li>" for skill in monster.skills.all()])
        html_content = f"""
                <html>
                <head>
                    <meta charset="UTF-8">
                </head>
                <body>
                    <h1>Monster: {monster.name}</h1>
                    <p><strong>Origin:</strong> {monster.origin}</p>
                    <p><strong>Challenge Rating:</strong> {monster.challenge_rating}</p>
                    <p><strong>Description:</strong> {monster.description}</p>

                    {image_html}

                    <h3>Combat Stats & Attributes:</h3>
                    <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; max-width: 500px;">
                        <tr>
                            <td><strong>Health Points (HP):</strong></td> <td>{monster.health_points}</td>
                            <td><strong>Armor Class (AC):</strong></td> <td>{monster.armor_class}</td>
                        </tr>
                        <tr>
                            <td><strong>Speed:</strong></td> <td>{monster.speed} m.</td>
                            <td><strong>Strength (STR):</strong></td> <td>{monster.strength}</td>
                        </tr>
                        <tr>
                            <td><strong>Dexterity (DEX):</strong></td> <td>{monster.dexterity}</td>
                            <td><strong>Constitution (CON):</strong></td> <td>{monster.constitution}</td>
                        </tr>
                        <tr>
                            <td><strong>Intelligence (INT):</strong></td> <td>{monster.intelligence}</td>
                            <td><strong>Wisdom (WIS):</strong></td> <td>{monster.wisdom}</td>
                        </tr>
                        <tr>
                            <td><strong>Charisma (CHA):</strong></td> <td>{monster.charisma}</td>
                            <td><strong>Views:</strong></td> <td>{monster.view_count}</td>
                        </tr>
                    </table>

                    <h3>Skills & Abilities:</h3>
                    <ul>
                        {skills_html}
                    </ul>
                </body>
                </html>
                """
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="monster_{monster.slug}.pdf"'
        return response


class ScenarioListView(ListView):
    model = Scenario
    template_name = 'compendium/scenario_list.html'
    context_object_name = 'scenario_list'


class ScenarioCreateView(CreateView):
    model = Scenario
    fields = ['title', 'description', 'starting_hook', 'monsters']
    template_name = 'compendium/scenario_form.html'
    success_url = reverse_lazy('compendium:scenario_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['monsters'].widget = forms.CheckboxSelectMultiple()
        form.fields['monsters'].queryset = Monster.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ScenarioDetailView(DetailView):
    model = Scenario
    template_name = 'compendium/scenario_detail.html'
    context_object_name = 'scenario_detail'


class ScenarioUpdateView(UpdateView):
    model = Scenario
    fields = ['title', 'description', 'starting_hook', 'monsters']
    template_name = 'compendium/scenario_form.html'
    success_url = reverse_lazy('compendium:scenario_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['monsters'].widget = forms.CheckboxSelectMultiple()
        form.fields['monsters'].queryset = Monster.objects.all()
        return form


class ScenarioDeleteView(DeleteView):
    model = Scenario
    template_name = 'compendium/scenario_delete.html'
    success_url = reverse_lazy('compendium:scenario_list')
