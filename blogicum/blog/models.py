from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse

from core.models import MetaModel

User = get_user_model()


class Post(MetaModel):
    title = models.CharField(
        'Заголовок', max_length=settings.MAX_HEAD_LENGHT
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def get_absolute_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.author.username}
        )

    def __str__(self):
        return self.title


class Category(MetaModel):
    title = models.CharField(
        'Заголовок', max_length=settings.MAX_HEAD_LENGHT
    )
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(MetaModel):
    name = models.CharField(
        'Название места', max_length=settings.MAX_HEAD_LENGHT
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField('Текст коментария')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        ordering = ('created_at',)

    def get_absolute_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.author.username}
        )
