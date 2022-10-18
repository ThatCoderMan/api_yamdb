import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


def get_current_year():
    return datetime.date.today().year


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(get_current_year())]
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, related_name='title')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='title', null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='review'
    )
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='review'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return (f'Обзор пользователя {self.author.username} '
                f'на произведение "{self.title}"')


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comment'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comment'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return ('Комментарий к обзору пользователя '
                f'{self.review.author.username} на '
                f'"{self.review.title}"')
