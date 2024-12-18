#!/usr/bin/python3
"""User related models."""
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    """User profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(
        upload_to='profile_pictures/', default='default_user_image.png')

    def __str__(self):
        return "{} Profile".format(self.user.username)
