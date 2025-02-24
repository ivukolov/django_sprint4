from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import (
    DetailView, 
    CreateView, 
    ListView, 
    UpdateView, 
    DeleteView
    )
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count

from blog.shortcuts import get_posts_query, get_category
from . models import Post, Comment, Category
from . forms import PostForm, CommentForm
from users.forms import BlogicumUserChangeForm

# Получаем модель пользователя.
BlogicumUser = get_user_model()


# def index(request):
#     """Главная страница проекта."""
#     post_list = get_posts_query()
#     template = 'blog/index.html'
#     context = {
#         'post_list': post_list[:settings.MAX_POSTS_LIMIT]
#     }
#     return render(request, template, context=context)


# def post_detail(request, post_id: int):
#     """Более развёрнутое представление поста."""
#     template = 'blog/detail.html'
#     post = get_object_or_404(get_posts_query(), pk=post_id)
#     context: dict = {
#         'post': post
#     }
#     return render(request, template, context=context)


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
    # queryset = Author.objects.all()

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(BlogicumUser, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author=self.object.pk)
        paginator = Paginator(posts, settings.MAX_POSTS_LIMIT)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IndexListView(ListView):
    model = Post
    paginate_by = settings.MAX_POSTS_LIMIT
    template_name = 'blog/index.html'

    def get_queryset(self):
        return Post.objects.prefetch_related(
            'comments'
        ).annotate(comment_count=Count('comments'))

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comment_count'] = Comment.objects.count()
    #     return context


class UserUpdateView(UpdateView):
    model = BlogicumUser
    form_class = BlogicumUserChangeForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.username}
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.kwargs.get('post_id'))
        return context


class PostUpdateView(UpdateView):
    """Класс для измения постов"""

    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'


class PostDeleteView(DeleteView):
    """Класс для удаления постов"""

    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class CommentCreateView(CreateView):
    post_model = None
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.post_model = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_model
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.post_model.id})
    

class CommentUpdateView(UpdateView):
    """Класс редактирования комментария"""
    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(DeleteView):
    """Класс удаления комментария"""
    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.id}
        )


class CategoryListView(ListView):
    """Класс для отображения категорий"""

    category = None
    template_name = 'blog/category.html'
    model = Post
    pk_url_kwarg = 'category_slug'
    paginate_by = settings.MAX_POSTS_LIMIT

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug=kwargs['category_slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        print(context['category'])
        return context
    
    def get_queryset(self):
        return Post.objects.prefetch_related(
            'comments'
        ).filter(category=self.category.pk).annotate(
            comment_count=Count('comments')
        )
