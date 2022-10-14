from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models

ROLES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class CustomManager():
    def _create_user(self, username, email, password=None, **other_fields):
        if not username:
            raise ValueError('The given username must be set.')
        if not email:
            raise ValueError('The given email must be set.')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **other_fields)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **other_fields):
        return self._create_user(username, email, password, **other_fields)

    def create_superuser(self, username, email, password=None, **other_fields):
        other_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **other_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(
        verbose_name='user name',
        max_length=255,
        validators=(RegexValidator(r'[\w.@+-]+\z')),
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='first name',
        max_lenth=255,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='last name',
        max_lenth=255,
        blank=True,
    )
    role = models.CharField(
        max_lenth=20,
        choices=ROLES,
        blank=True,
        default='user',
    )
    bio = models.TextField(
        verbose_name='biography description',
        blank=True,
    )
    confirmation_code = models.CharField(
        verbose_name='confirnmation_code',
        max_lenth=20,
        blank=True,
    )
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'email',)
    objects = CustomManager()
