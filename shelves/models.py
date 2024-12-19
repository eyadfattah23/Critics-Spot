#!/usr/bin/python3
"""Shelves related models."""
from django.db import models
from django.conf import settings
from books.models import Book

# Create your models here.


class Shelf(models.Model):
    """Model to represent a user's book shelf."""
    DEFAULT_SHELVES = ['Read', 'Reading', 'Want To Read']

    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # Distinguish between default and custom shelves
    is_default = models.BooleanField(default=False)

    class Meta:
        # User cannot have duplicate shelf names
        unique_together = ('name', 'user')
        indexes = [
            models.Index(fields=['name', 'user']),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class ShelfBook(models.Model):
    """Model representing a book in a shelf."""
    shelf = models.ForeignKey(
        Shelf, on_delete=models.CASCADE0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        # Prevent duplicate books in the same shelf
        unique_together = ('shelf', 'book')
        indexes = [
            models.Index(fields=['shelf', 'book']),
        ]

    def __str__(self):
        return f"{self.book.title} in {self.shelf.name} owned by user: ({self.shelf.user.username})"
