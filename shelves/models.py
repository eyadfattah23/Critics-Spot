#!/usr/bin/python3
"""Shelves related models."""
import os
from django.db import models
from django.conf import settings
from books.models import Book
# Create your models here.


def shelf_image_upload_to(instance, filename):
    """Generate file path for shelf cover images."""
    ext = filename.split('.')[-1]
    return os.path.join(
        f"shelf_covers/{instance.user.username}/{instance.name}/cover.{ext}")


class Shelf(models.Model):
    """Model representing a shelf."""

    DEFAULT_SHELVES = ['Read', 'Currently Reading',
                       'Want To Read', 'Favorites']

    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shelves',
                             on_delete=models.CASCADE)
    # Distinguish between default and custom shelves

    image = models.ImageField(
        upload_to=shelf_image_upload_to,
        null=True,
        blank=True,
        help_text="Cover image for the shelf"
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        """Meta options for Shelf model."""

        # User cannot have duplicate shelf names
        unique_together = ('name', 'user')
        indexes = [
            models.Index(fields=['name', 'user']),
        ]

    def __str__(self):
        """Return string representation of the Shelf model."""
        return (
            f'shelf "{self.name}":{self.pk} owned by '
            f'"{self.user.username}":{self.user.pk}'
        )


class ShelfBook(models.Model):
    """Model representing a book on a shelf."""

    shelf = models.ForeignKey(
        Shelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    current_page = models.PositiveIntegerField(default=0)  # Add this field
    notes = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True, blank=True)

    @property
    def reading_progress(self):
        """Calculate reading progress percentage."""
        if self.book.pages:
            return round((self.current_page / self.book.pages) * 100, 1)
        return 0

    class Meta:
        """Meta options for ShelfBook model."""

        # Prevent duplicate books in the same shelf
        unique_together = ('shelf', 'book')
        indexes = [
            models.Index(fields=['shelf', 'book']),
        ]

    def __str__(self):
        """Return string representation of the ShelfBook model."""
        return (
            f"{self.book.title}|{self.book.id} in {self.shelf.name}|{self.shelf.id} "
            f"owned by user: ({self.shelf.user.username})|{self.shelf.user.id}"
        )
