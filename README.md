# django_sprint4
 
1 AssertionError: Убедитесь, что на странице категории не отображаются посты, снятые с публикации.
2 Убедитесь, что на странице категории не отображаются публикации других категорий.
3 Убедитесь, что страница категории недоступна, если категория снята с публикации.
4 Убедитесь, что на странице категории не отображаются отложенные публикации.

5 ssertionError: Проверьте view-функции приложения `pages`: убедитесь, что для генерации страниц со статусом ответа `{status}` используется шаблон `pages/{fname}`
E           assert '404.html' in "from django.views.generic import TemplateView\n\n\nclass About(TemplateView):\n\n    template_name = 'pages/about.html'\n\n\nclass Rules(TemplateView):\n\n    template_name = 'pages/rules.html'\n"
E            +  where "from django.views.generic import TemplateView\n\n\nclass About(TemplateView):\n\n    template_name = 'pages/about.html'\n\n\nclass Rules(TemplateView):\n\n    template_name = 'pages/rules.html'\n" = <function getsource at 0x7fbfa4173d80>(<module 'pages.views' from '/home/i.vukolov@vrgaz.ru/Документы/Dev/Jango/django_sprint4/blogicum/pages/views.py'>)
E            +    where <function getsource at 0x7fbfa4173d80> = inspect.getsource

6 AssertionError: Убедитесь, что подключены маршруты для работы с пользователями из `django.contrib.auth.urls`.
_________________________
7 self = <blog.views.UserUpdateView object at 0x7fbfa0d78f10>

    def get_success_url(self):
        return reverse_lazy(
>           'blog:profile', kwargs={'username': self.username}
        )
E       AttributeError: 'UserUpdateView' object has no attribute 'username'

_______________
8 self = <blog.views.UserUpdateView object at 0x7fbfa0d78f10>

    def get_success_url(self):
        return reverse_lazy(
>           'blog:profile', kwargs={'username': self.username}
        )
E       AttributeError: 'UserUpdateView' object has no attribute 'username'
