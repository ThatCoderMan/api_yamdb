import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def get_current_year():
    return datetime.date.today().year


class Categories(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genres(models.Model):
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
    genre = models.ForeignKey(
        Genres, on_delete=models.SET_NULL,
        related_name='title', null=True
    )
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL,
        related_name='title', null=True
    )

    def __str__(self):
        return self.name
