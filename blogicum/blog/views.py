from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
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
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils import timezone

from . models import Post, Comment, Category
from . forms import PostForm, CommentForm
from users.forms import BlogicumUserChangeForm

# Получаем модель пользователя.
BlogicumUser = get_user_model()


class OnlyAuthorMixin(UserPassesTestMixin):
    """Класс для подмешивания проверки доступа"""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user
    
    def handle_no_permission(self):
        return redirect('blog:post_detail', post_id=self.kwargs.get('post_id'))


class ListViewMixin:
    """"Класс для подмешивания спсика постов"""

    model = Post
    paginate_by = settings.MAX_POSTS_LIMIT

    def get_queryset(self):
        return Post.objects.annotate(
            comment_count=Count('comments')
        ).order_by(*Post._meta.ordering)

    def _get_cdate(self):
        """Метод для определения текущего времени."""
        return timezone.now()


class ProfileDetailView(ListViewMixin, ListView):
    """Класс для отображения страницы пользователя"""

    user_model = None
    template_name = 'blog/profile.html'

    def dispatch(self, request, *args, **kwargs):
        self.user_model = get_object_or_404(BlogicumUser, username=kwargs['username'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(author=self.user_model.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.user_model
        return context


class PostCreateView(LoginRequiredMixin, CreateView,):
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

    def get_queryset(self):
        return super().get_queryset().filter(
            pub_date__lte=self._get_cdate(),
            is_published=True,
            category__is_published=True
        )


class UserUpdateView(LoginRequiredMixin, UpdateView):
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


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    """Класс для измения постов"""

    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    """Класс для удаления постов"""

    template_name = 'blog/create.html'
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
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


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    """Класс редактирования комментария"""

    template_name = 'blog/comment.html'
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.post.id}
        )


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
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
