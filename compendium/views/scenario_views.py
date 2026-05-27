import os

from django import forms
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.core.mail import send_mass_mail
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

from compendium.models import Scenario, Monster, Subscriber
from config import settings


@method_decorator(never_cache, name='dispatch')
class ScenarioListView(
    ListView
):
    model = Scenario
    template_name = 'compendium/scenarios_templates/scenario_list.html'
    context_object_name = 'scenario_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_scenarios'] = Scenario.objects.order_by(
            '-view_count', 'title'
        )[:3]
        return context


class ScenarioSearchView(
    ListView
):
    model = Scenario
    template_name = ('compendium/scenarios_templates/'
                     'scenario_search_results.html')
    context_object_name = 'scenario_list'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            return Scenario.objects.filter(title__icontains=query)
        return Scenario.objects.all()


class ScenarioCreateView(
    LoginRequiredMixin,
    CreateView
):
    model = Scenario
    fields = ['title', 'description', 'starting_hook', 'monsters']
    template_name = ('compendium/scenarios_templates/'
                     'scenario_form.html')
    success_url = reverse_lazy('compendium:scenario_list')

    def notify_subscribers(self, scenario):
        emails = list(Subscriber.objects.values_list('email', flat=True))
        if not emails:
            return
        subject = f"[Pirates Compendium] New Scenario: {scenario.title}"
        message = (
            f"A new scenario has been added!\n\n"
            f"Title: {scenario.title}\n\n"
            f"Description:\n{scenario.description}\n\n"
            f"Starting Hook:\n{scenario.starting_hook}\n\n"
            f"View it here: {settings.SITE_URL}/scenario/{scenario.slug}/"
        )
        from_email = os.getenv('GMAIL_SENDER_EMAIL')
        email_tuples = tuple(
            (subject, message, from_email, [email]) for email in emails
        )
        send_mass_mail(email_tuples, fail_silently=True)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['monsters'].widget = forms.CheckboxSelectMultiple()
        form.fields['monsters'].queryset = Monster.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        self.notify_subscribers(self.object)
        return response


@method_decorator(never_cache, name='dispatch')
class ScenarioDetailView(
    DetailView
):
    model = Scenario
    template_name = ('compendium/scenarios_templates/'
                     'scenario_detail.html')
    context_object_name = 'scenario_detail'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.view_count = F('view_count') + 1
        obj.save(update_fields=['view_count'])
        obj.refresh_from_db()
        return obj


class ScenarioUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Scenario
    fields = ['title', 'description', 'starting_hook', 'monsters']
    template_name = ('compendium/scenarios_templates/'
                     'scenario_form.html')
    success_url = reverse_lazy('compendium:scenario_list')

    def test_func(self):
        scenario = self.get_object()
        return self.request.user == scenario.author

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['monsters'].widget = forms.CheckboxSelectMultiple()
        form.fields['monsters'].queryset = Monster.objects.all()
        return form


class ScenarioDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Scenario
    template_name = ('compendium/scenarios_templates/'
                     'scenario_delete.html')
    success_url = reverse_lazy('compendium:scenario_list')

    def test_func(self):
        scenario = self.get_object()
        return self.request.user == scenario.author


class ScenarioPdfView(
    DetailView
):
    model = Scenario

    def render_to_response(self, context, **response_kwargs):
        scenario = self.object
        html_content = render_to_string(
            'compendium/scenarios_templates/scenario_pdf.html',
            {'scenario': scenario}
        )
        pdf_file = HTML(string=html_content).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="scenario_{scenario.slug}.pdf"'
        )
        return response
