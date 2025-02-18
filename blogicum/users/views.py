from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.conf import settings

from .forms import BlogicumUserCreationForm


class BlogicumCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = BlogicumUserCreationForm
    success_url = settings.LOGIN_REDIRECT_URL
