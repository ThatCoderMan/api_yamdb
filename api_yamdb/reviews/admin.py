from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category', 'view_genre_list')
    ordering = ('name',)
    list_filter = ('year', 'category', 'genre', )
    search_fields = ('name__startswith',
                     'year',
                     'category__name__startswith',
                     'genre__name__startswith')

    def view_genre_list(self, obj):
        genres = Title.genre.through.objects.filter(title_id=obj.id)
        genre_list = ''
        for genre in genres:
            genre = Genre.objects.get(pk=genre.genre_id)
            genre_list += genre.name + ' '
        return genre_list
    view_genre_list.short_description = 'Genres'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name__startswith',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name__startswith',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'author', 'text', 'pub_date')
    ordering = ('-pub_date',)
    list_filter = ('title', 'author', )
    search_fields = ('title__name__startswith',
                     'score',
                     'author__username__startswith',
                     'text')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date')
    ordering = ('-pub_date',)
    list_filter = ('author', 'review__title')
    search_fields = ('review__author__username__startswith',
                     'author__username__startswith',
                     'text')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role',)
    search_fields = ('username__startswith',
                     'email__startswith',
                     'first_name__startswith',
                     'last_name__startswith',
                     'role__startswith')
