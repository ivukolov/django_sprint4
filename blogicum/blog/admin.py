from django.contrib import admin

from .models import (
    Category,
    Comment,
    Location,
    Post,
)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'is_published',
        'category',
        'created_at',
    )
    list_editable = (
        'pub_date',
        'is_published',
        'category',
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('is_published',)
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'created_at',
        'author',
        'post',
    )
    search_fields = ('text',)
