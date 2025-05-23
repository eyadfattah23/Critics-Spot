# Generated by Django 5.1.4 on 2025-01-07 08:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='books_genre_name_27aecb_idx'),
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(related_name='books', to='books.genre'),
        ),
        migrations.AddIndex(
            model_name='bookreview',
            index=models.Index(fields=['user', 'book'], name='books_bookr_user_id_e526f9_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='bookreview',
            unique_together={('user', 'book')},
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['title'], name='books_book_title_d3218d_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['author'], name='books_book_author__709385_idx'),
        ),
        migrations.AddIndex(
            model_name='book',
            index=models.Index(fields=['slug'], name='books_book_slug_ca552e_idx'),
        ),
    ]
