from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_me_as_username

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='user name',
        max_length=150,
        validators=(
            RegexValidator(r'[\w.@+-]+'),
            validate_me_as_username,
        ),
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_length=150,
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        blank=True,
        default='user',
    )
    bio = models.TextField(
        verbose_name='biography description',
        blank=True,
    )
    confirmation_code = models.CharField(
        verbose_name='confirmation_code',
        max_length=50,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def save(self, *args, **kwargs):
        if self.is_admin or self.is_superuser:
            self.is_staff = True
        else:
            self.is_staff = False
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
