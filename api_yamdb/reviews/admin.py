from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .cauth_forms import CustomUserChangeForm, CustomUserCreationForm
from .cauth_models import CustomUser
from .models import Category, Comment, Genre, Review, Title

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'username', 'is_superuser',)
    list_filter = ('role', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'email',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio',)}),
        ('Permissions', {'fields': ('role', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
