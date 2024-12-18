#!/usr/bin/python3
"""Book related models."""
from django.db import models


class Author(models.Model):
    """Author model."""

    name = models.CharField(max_length=128)
    birth_date = models.DateField()
    death_date = models.DateField(null=True)  # maybe still alive
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/',
                              default='default_author.png')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        """Return the name of the author.

        Returns:
            str: string representation of the author
        """
        return self.name


class Book(models.Model):
    """Book model."""

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True)
    publication_date = models.DateField()
    pages = models.IntegerField()  # for limiting the current_page feature
    cover = models.ImageField(upload_to='covers/', default='default_book.png')
    buy_link = models.CharField(max_length=255, null=True)
    # avg_rating
    description = models.TextField(blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default='-')  # for search

    # isbn = models.CharField(max_length=13)  # maybe make this a primary key
    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
        ordering = ["-added_date"]

    def __str__(self):
        """Return the title of the book.

        Returns:
            str: string representation of the book
        """
        return self.title
