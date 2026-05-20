from django import forms

from compendium.models import Skill, DevilFruit


class DevilFruitForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple, required=True, label="Add skills")

    class Meta:
        model = DevilFruit
        fields = ['name', 'slug', 'fruit_type', 'description', 'image', 'skills']