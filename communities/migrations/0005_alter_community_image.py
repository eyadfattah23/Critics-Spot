# Generated by Django 5.1.4 on 2024-12-23 18:12

import communities.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_remove_community_posts_community_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='image',
            field=models.ImageField(default='default_community_image.jpeg', upload_to=communities.models.community_image_upload_to),
        ),
    ]
