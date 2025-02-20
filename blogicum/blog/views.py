from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import DetailView

from blog.shortcuts import get_posts_query, get_category
from users.models import BlogicumUser


def index(request):
    """Главная страница проекта."""
    post_list = get_posts_query()
    template = 'blog/index.html'
    context = {
        'post_list': post_list[:settings.MAX_POSTS_LIMIT]
    }
    return render(request, template, context=context)


def post_detail(request, post_id: int):
    """Более развёрнутое представление поста."""
    template = 'blog/detail.html'
    post = get_object_or_404(get_posts_query(), pk=post_id)
    context: dict = {
        'post': post
    }
    return render(request, template, context=context)


def category_posts(request, category_slug: str):
    """Фильтрация постов по категории."""
    template = 'blog/category.html'
    category = get_category(category_slug)
    posts = get_posts_query().filter(category__slug=category_slug)
    context = {
        'post_list': posts,
        'category': category
    }
    return render(request, template, context=context)


class ProfileDetailView(DetailView):
    model = BlogicumUser
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(BlogicumUser, username=username)
