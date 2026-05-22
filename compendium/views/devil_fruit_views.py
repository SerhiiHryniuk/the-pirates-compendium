from django import forms
from django.db.models import F
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from weasyprint import HTML

from compendium.models import (
    DevilFruit,
    Skill
)


class DevilFruitListView(ListView):
    model = DevilFruit
    template_name = 'compendium/devil_fruits_templates/devil_fruit_list.html'
    context_object_name = 'devil_fruit_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_devil_fruits'] = DevilFruit.objects.order_by(
            '-view_count', 'name'
        )[:3]
        return context


class DevilFruitSearchView(ListView):
    model = DevilFruit
    template_name = 'compendium/devil_fruits_templates/devil_fruit_search_results.html'
    context_object_name = 'devil_fruit_list'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get(
            'search',
            ''
        )
        if query:
            return DevilFruit.objects.filter(
                name__icontains=query
            )
        return DevilFruit.objects.all()


class DevilFruitCreateView(CreateView):
    model = DevilFruit
    fields = ['name', 'fruit_type', 'description', 'image', 'skills']
    template_name = 'compendium/devil_fruits_templates/devil_fruit_form.html'
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
    template_name = 'compendium/devil_fruits_templates/devil_fruit_detail.html'
    context_object_name = 'devil_fruit_detail'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count = F('view_count') + 1
        obj.save(update_fields=['view_count'])
        obj.refresh_from_db()
        return obj


class DevilFruitUpdateView(UpdateView):
    model = DevilFruit
    fields = ['name', 'fruit_type', 'description', 'image', 'skills']
    template_name = 'compendium/devil_fruits_templates/devil_fruit_form.html'
    success_url = reverse_lazy('compendium:devil_fruit_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form


class DevilFruitDeleteView(DeleteView):
    model = DevilFruit
    template_name = 'compendium/devil_fruits_templates/devil_fruit_delete.html'
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
