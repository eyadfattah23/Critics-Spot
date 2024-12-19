#!/usr/bin/python3
"""User related models."""
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    """User profile model"""
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(
        upload_to='profile_pictures/', default='default_user_image.png')

    def __str__(self):
        return "{} Profile".format(self.user.username)
