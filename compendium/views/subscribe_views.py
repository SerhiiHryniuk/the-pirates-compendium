from django.contrib import messages
from django.shortcuts import redirect
from django.views import View

from compendium.forms import SubscriberForm
from compendium.models import Subscriber


class SubscribeView(View):
    http_method_names = ['post']

    def post(self, request):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            _, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "You're subscribed! You'll get notified on new scenarios.")
            else:
                messages.info(request, "This email is already subscribed.")
        else:
            messages.error(request, "Please enter a valid email address.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
