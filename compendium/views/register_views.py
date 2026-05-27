from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from compendium.forms import RegisterForm


class RegisterView(View):
    template_name = 'compendium/registration/register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('compendium:index')
        return render(request, self.template_name, {'form': form})
