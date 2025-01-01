#!usr/bin/python3
"""Book related filters."""

from django_filters.rest_framework import FilterSet
from django_filters import filters, IsoDateTimeFilter
from django.db import models as django_models
from .models import *


class BookFilter(FilterSet):
    """Book filter."""

    genres = filters.CharFilter(method='filter_by_multiple_genres')

    class Meta:
        model = Book
        fields = {
            'title': ['icontains', 'exact'],
            'author__name': ['icontains'],
            'publication_date': ['year__gt', 'year__lt'],
            'avg_rating': ['gt', 'lt'],
        }

    def filter_by_multiple_genres(self, queryset, name, value):
        """
        Filter books by multiple genres (comma-separated).
        """
        genre_list = value.split(",")  # Split the input into a list
        return queryset.filter(genres__name__in=genre_list).distinct()


class AuthorFilter(FilterSet):
    """Author filter."""

    class Meta:
        model = Author
        fields = {
            'name': ['icontains'],
            'birth_date': ['year__gt', 'year__lt'],
            'death_date': ['year__gt', 'year__lt'],
        }


class GenreFilter(FilterSet):
    """Genre filter."""

    class Meta:
        model = Genre
        fields = {
            'name': ['icontains'],
        }


class BookReviewFilter(FilterSet):
    """Book review filter."""

    class Meta:
        model = BookReview
        fields = {
            'user__username': ['icontains'],
            'book__title': ['icontains'],
            'created_at': ['gte', 'lte'],
            'rating': ['gte', 'lte']
        }
    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': IsoDateTimeFilter
        },
    }
