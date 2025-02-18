from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone

from blog.models import Post, Category


def __get_cdate():
    """Функция для определения текущего времени."""
    return timezone.now()


def get_posts_query() -> QuerySet:
    """Функция возращяет Queryset актуальных постов."""
    current_date = __get_cdate()
    return Post.objects.select_related(
        'category', 'location'
    ).filter(
        pub_date__lte=current_date,
        is_published=True,
        category__is_published=True
    )


def get_category(category_slug: str) -> Category:
    """Функция возвращяет информацию о категории либо 404."""
    category: Category = get_object_or_404(
        Category.objects.values(
            'title', 'description'
        ).filter(is_published=True), slug=category_slug
    )
    return category
