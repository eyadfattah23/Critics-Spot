#!/usr/bin/python3
"""Book related models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
import re


def validate_isbn(value):
    """Validate ISBN-13 format."""
    if not re.match(r'^(?=(?:\D*\d){13}(?:(?:\D*\d){0})?$)[\d-]+$', value.replace("-", "")):
        raise ValidationError('Invalid ISBN format. Must be ISBN-13 format.')


def validate_future_date(value):
    """Validate that date is not in the future."""
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')


def validate_death_date(value):
    """Validate death date is after birth date."""
    if hasattr(value, 'birth_date') and value < value.birth_date:
        raise ValidationError('Death date must be after birth date.')


class Author(models.Model):
    """Author model."""
    name = models.CharField(max_length=128)
    birth_date = models.DateField(validators=[validate_future_date])
    death_date = models.DateField(
        null=True,
        blank=True,
        validators=[validate_future_date, validate_death_date]
    )
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='authors_pics/',
                              default='default_author.png')
    added_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=128, unique=True, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.death_date and self.death_date < self.birth_date:
            raise ValidationError('Death date must be after birth date.')

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Genre model."""

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)
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
        return f"{self.name}"


class Book(models.Model):
    """Book model."""

    title = models.CharField(max_length=255, unique=True)
    buy_link = models.URLField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True)
    pages = models.PositiveIntegerField()  # for limiting the current_page feature
    publication_date = models.DateField(validators=[validate_future_date])
    added_date = models.DateTimeField(auto_now_add=True)
    cover = models.ImageField(upload_to='covers/', default='default_book.png')

    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, null=True, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')

    avg_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(
            Decimal('0.00')), MaxValueValidator(Decimal('5.00'))]
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    # isbn = models.CharField(max_length=13)  # maybe make this a primary key

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['author']),
            models.Index(fields=['slug'])
        ]
        ordering = ["-added_date", 'title']

    def __str__(self):
        """Return the title of the book.

        Returns:
            str: string representation of the book
        """
        return "{}|{}, by: {}|{}".format(self.title, self.pk, self.author, self.author.id)
