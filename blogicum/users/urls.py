from django.urls import path

from . import views

urlpatterns = [
    path(
        'registration/',
        views.BlogicumCreateView.as_view(),
        name='registration'
    ),
]
