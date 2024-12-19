# Generated by Django 5.1.4 on 2024-12-19 19:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        ('shelves', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shelf',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shelfbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book'),
        ),
        migrations.AddField(
            model_name='shelfbook',
            name='shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shelves.shelf'),
        ),
        migrations.AddIndex(
            model_name='shelf',
            index=models.Index(fields=['name', 'user'], name='shelves_she_name_3d5126_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='shelf',
            unique_together={('name', 'user')},
        ),
        migrations.AddIndex(
            model_name='shelfbook',
            index=models.Index(fields=['shelf', 'book'], name='shelves_she_shelf_i_dd77ec_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='shelfbook',
            unique_together={('shelf', 'book')},
        ),
    ]
