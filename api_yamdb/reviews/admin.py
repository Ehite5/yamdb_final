from django.contrib import admin

from .models import User, Category, Genre, Title, Review


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'role',
        'email',
        'bio',
        'confirmation_code',
    )
    search_fields = ('username',)
    list_filter = ('username', 'role',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Review)
