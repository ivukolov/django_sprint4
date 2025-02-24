from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth import get_user_model
from django.db.models import Count

from . models import Post, Comment, Category
from . forms import PostForm, CommentForm
from users.forms import BlogicumUserChangeForm

# Получаем модель пользователя.
BlogicumUser = get_user_model()


class ListViewMixin:
    """Миксин для отображения спсика постов"""

    model = Post
    paginate_by = settings.MAX_POSTS_LIMIT

    def get_queryset(self):
        return Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by(*Post._meta.ordering)


class ProfileDetailView(ListViewMixin, ListView):
    """Класс для отображения страницы пользователя"""

    template_name = 'blog/profile.html'

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = BlogicumUser.objects.get(
            username=self.request.user
        )
        return context


class PostCreateView(CreateView):
    """Класс для создания постов"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IndexListView(ListViewMixin, ListView):
    """Класс для представления главной страницы"""

    template_name = 'blog/index.html'


class UserUpdateView(UpdateView):
    """Класс для обновление страницы пользователя"""

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
    """Класс для развёрнутого представения поста"""

    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(
            post=self.kwargs.get('post_id')
        )
        return context


class PostUpdateView(UpdateView):
    """Класс для измения постов"""

    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')


class PostDeleteView(DeleteView):
    """Класс для удаления постов"""

    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class CommentCreateView(CreateView):
    """Класс для создания комментариев к посту"""

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
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.post_model.id}
        )


class CommentUpdateView(UpdateView):
    """Класс редактирования комментария"""

    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.post.id}
        )


class CommentDeleteView(DeleteView):
    """Класс удаления комментария"""

    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.post.id}
        )


class CategoryListView(ListViewMixin, ListView):
    """Класс для отображения категорий"""

    category = None
    template_name = 'blog/category.html'
    pk_url_kwarg = 'category_slug'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category, slug=kwargs['category_slug']
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        print(context['category'])
        return context
