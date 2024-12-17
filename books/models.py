#!/usr/bin/python3
"""Book related models."""
from django.db import models


class Book(models.Model):
    """Book model."""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=128)  # change when author is created
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)  # maybe make this a primary key
    pages = models.IntegerField()
    cover = models.ImageField(upload_to='covers/', default='default_book.png')
    buy_link = models.CharField(max_length=255, null=True)
    # avg_rating
    description = models.TextField(blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
        ordering = ["-added_date"]

    def __str__(self):
        return self.title
