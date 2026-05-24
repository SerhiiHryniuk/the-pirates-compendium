import base64
import requests as http_requests

from django import forms
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
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

from compendium.models import (
    DevilFruit,
    Skill
)


@method_decorator(never_cache, name='dispatch')
class DevilFruitListView(
    ListView
):
    model = DevilFruit
    template_name = ('compendium/devil_fruits_templates/'
                     'devil_fruit_list.html')
    context_object_name = 'devil_fruit_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_devil_fruits'] = DevilFruit.objects.order_by(
            '-view_count', 'name'
        )[:3]
        return context


class DevilFruitSearchView(
    ListView
):
    model = DevilFruit
    template_name = ('compendium/devil_fruits_templates/'
                     'devil_fruit_search_results.html')
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


class DevilFruitCreateView(
    LoginRequiredMixin,
    CreateView
):
    model = DevilFruit
    fields = ['name', 'fruit_type', 'description', 'image', 'skills']
    template_name = ('compendium/devil_fruits_templates/'
                     'devil_fruit_form.html')
    success_url = reverse_lazy(
        'compendium:devil_fruit_list'
    )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@method_decorator(never_cache, name='dispatch')
class DevilFruitDetailView(
    DetailView
):
    model = DevilFruit
    template_name = ('compendium/devil_fruits_templates/'
                     'devil_fruit_detail.html')
    context_object_name = 'devil_fruit_detail'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count = F('view_count') + 1
        obj.save(update_fields=['view_count'])
        obj.refresh_from_db()
        return obj


class DevilFruitUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = DevilFruit
    fields = ['name', 'fruit_type', 'description', 'image', 'skills']
    template_name = ('compendium/devil_fruits_templates/'
                     'devil_fruit_form.html')
    success_url = reverse_lazy(
        'compendium:devil_fruit_list'
    )

    def test_func(self):
        devil_fruit = self.get_object()
        return self.request.user == devil_fruit.author

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['skills'].widget = forms.CheckboxSelectMultiple()
        form.fields['skills'].queryset = Skill.objects.all()
        return form


class DevilFruitDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = DevilFruit
    template_name = ('compendium/devil_fruits_templates/'
                     'devil_fruit_delete.html')
    success_url = reverse_lazy(
        'compendium:devil_fruit_list'
    )

    def test_func(self):
        devil_fruit = self.get_object()
        return self.request.user == devil_fruit.author


class DevilFruitPdfView(DetailView):
    model = DevilFruit

    def render_to_response(self, context, **response_kwargs):
        fruit = self.object

        image_data = None
        image_content_type = None
        if fruit.image:
            try:
                img_response = http_requests.get(fruit.image.url)
                image_data = base64.b64encode(img_response.content).decode('utf-8')
                image_content_type = img_response.headers.get('Content-Type', 'image/jpeg')
            except Exception:
                pass

        html_content = render_to_string(
            'compendium/devil_fruits_templates/devil_fruit_pdf.html',
            {
                'fruit': fruit,
                'image_data': image_data,
                'image_content_type': image_content_type,
            }
        )
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="devil_fruit_{fruit.slug}.pdf"'
        return response
