#!/usr/bin/python3
"""User related models."""
from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Book
# Create your models here.


class CustomUser(AbstractUser):
    """User profile model"""
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(
        upload_to='profile_pictures/', default='default_user_image.png')

    def __str__(self):
        return "{} Profile".format(self.username)


class Favorite(models.Model):
    """Model to represent a user's favorite books."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        # Prevent duplicate books in the same shelf
        unique_together = ('user', 'book')
        indexes = [
            models.Index(fields=['user', 'book']),
        ]

    def __str__(self):
        return f"{self.book.title} is a favorite of {self.user.username}"


class BookReview(models.Model):
    """Model to represent a user's book review."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate books in the same shelf
        unique_together = ('user', 'book')
        indexes = [
            models.Index(fields=['user', 'book']),
        ]

    def __str__(self):
        return f"{self.user.username} reviewed {self.book.title} at {self.created_at}"
