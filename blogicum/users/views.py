from django.views.generic.edit import CreateView
from django.conf import settings
from django.urls import reverse_lazy

from .forms import BlogicumUserCreationForm


class BlogicumCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = BlogicumUserCreationForm
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
