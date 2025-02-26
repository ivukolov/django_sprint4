from django.shortcuts import render
from django.views.generic import TemplateView


def custom_500(request):
    return render(request, 'pages/500.html', status=500)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


# class Custom404View(TemplateView):
#     template_name = 'pages/404.html'

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context, status=404)


# class Custom500View(TemplateView):
#     template_name = 'pages/500.html'

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context, status=500)


# class Custom403View(TemplateView):
#     template_name = 'pages/403.html'

#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return self.render_to_response(context, status=403)

