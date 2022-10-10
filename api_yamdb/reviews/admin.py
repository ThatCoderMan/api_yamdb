from django.contrib import admin

from .models import Categories, Genres, Title

admin.site.register(Title)
admin.site.register(Categories)
admin.site.register(Genres)
