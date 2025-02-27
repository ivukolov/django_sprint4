from django.views.generic import TemplateView
from django.shortcuts import render
from http import HTTPStatus


class About(TemplateView):

    template_name = 'pages/about.html'


class Rules(TemplateView):

    template_name = 'pages/rules.html'


def custom_500(request):
    return render(
        request, 'pages/500.html', status=HTTPStatus.INTERNAL_SERVER_ERROR
    )


def page_not_found(request, exception):
    return render(
        request, 'pages/404.html', status=HTTPStatus.NOT_FOUND
    )


def csrf_failure(request, reason=''):
    return render(
        request, 'pages/403csrf.html', status=HTTPStatus.FORBIDDEN
    )
