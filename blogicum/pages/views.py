from django.shortcuts import render


def about(request):
    """О проекте
    template: str - шаблон html старницы
    """
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    """Наши правила
    template: str - шаблон html старницы
    """
    template = 'pages/rules.html'
    return render(request, template)
