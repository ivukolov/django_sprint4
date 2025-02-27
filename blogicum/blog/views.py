from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from users.forms import BlogicumUserChangeForm

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

BlogicumUser = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    """Класс для подмешивания проверки доступа."""

    def test_func(self):
        _obj = self.get_object()
        return _obj.author == self.request.user

    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs.get('post_id'))


class PostRedirectMixin:
    """Миксин для lazy redirect по индексу."""

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class TimeGetMixin:
    """Миксин для определения текущего времени."""

    def _get_cdate(self):
        return timezone.now()


class OnlyAuthorUpdateMixin(TimeGetMixin):
    """Миксин для подмешивания проверки авторства и валидности данных."""

    def get_object(self, queryset=None):
        obj = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        if obj.author == self.request.user:
            return obj
        if (
            obj.pub_date <= self._get_cdate()
            and obj.is_published
            and obj.category.is_published
        ):
            return obj
        raise Http404


class ListViewMixin(TimeGetMixin):
    """Класс для подмешивания спсика постов."""

    model = Post
    paginate_by = settings.MAX_POSTS_LIMIT

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'location', 'category'
        ).annotate(
            comment_count=Count('comments')
        ).order_by(*Post._meta.ordering)


class ProfileDetailView(ListViewMixin, ListView):
    """Класс для отображения страницы пользователя."""

    user_obj = None
    template_name = 'blog/profile.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_obj = get_object_or_404(
            BlogicumUser, username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.user_obj.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user_obj
        return context


class PostCreateView(LoginRequiredMixin, CreateView,):
    """Класс для создания постов."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IndexListView(OnlyAuthorUpdateMixin, ListViewMixin, ListView):
    """Класс для представления главной страницы."""

    template_name = 'blog/index.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            pub_date__lte=self._get_cdate(),
            is_published=True,
            category__is_published=True
        )


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для обновление страницы пользователя."""

    model = BlogicumUser
    form_class = BlogicumUserChangeForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )


class PostDetailView(OnlyAuthorUpdateMixin, DetailView):
    """Класс для развёрнутого представения поста."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(
            post=self.kwargs.get('post_id')
        )
        return context


class PostUpdateView(OnlyAuthorUpdateMixin, OnlyAuthorMixin, UpdateView):
    """Класс для измения постов."""

    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Класс для удаления постов."""

    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class CommentCreateView(PostRedirectMixin, LoginRequiredMixin, CreateView):
    """Класс для создания комментариев к посту."""

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


class CommentUpdateView(PostRedirectMixin, OnlyAuthorMixin, UpdateView):
    """Класс редактирования комментария."""

    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'


class CommentDeleteView(PostRedirectMixin, OnlyAuthorMixin, DeleteView):
    """Класс удаления комментария."""

    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'


class CategoryListView(ListViewMixin, ListView):
    """Класс для отображения категорий."""

    model = Category
    category = None
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category, slug=kwargs['category_slug'], is_published=True
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(
            pub_date__lte=self._get_cdate(),
            is_published=True,
            category__is_published=True,
            category=self.category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
