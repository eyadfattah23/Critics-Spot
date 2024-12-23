#!/usr/bin/python3
"""Book related models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Author(models.Model):
    """Author model."""

    name = models.CharField(max_length=128)
    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)  # maybe still alive
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='authors_pics/',
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


class Genre(models.Model):
    """Genre model."""

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        """Return the name of the genre.

        Returns:
            str: string representation of the genre
        """
        return self.name


class Book(models.Model):
    """Book model."""

    title = models.CharField(max_length=255, unique=True)
    buy_link = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True)
    pages = models.PositiveIntegerField()  # for limiting the current_page feature
    publication_date = models.DateField()
    added_date = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='covers/', default='default_book.png')

    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True)
    genres = models.ManyToManyField(Genre)

    avg_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(
            Decimal('0.00')), MaxValueValidator(Decimal('5.00'))]
    )

    # isbn = models.CharField(max_length=13)  # maybe make this a primary key
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author'])
        ]
        ordering = ["-added_date", 'title']

    def __str__(self):
        """Return the title of the book.

        Returns:
            str: string representation of the book
        """
        return "{}|{}".format(self.title, self.author)
