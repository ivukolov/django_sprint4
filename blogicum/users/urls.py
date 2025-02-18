from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path(
        'registration/',
        views.BlogicumCreateView.as_view(),
        name='registration'
    ),
]
