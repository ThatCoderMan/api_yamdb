# Generated by Django 2.2.16 on 2022-10-18 17:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='review', to='reviews.Title'
            ),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='comment', to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='reviews.Review'
            ),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_title_author'),
        ),
    ]
