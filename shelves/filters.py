#!usr/bin/python3
"""Shelves related filters."""

import django_filters
from .models import Shelf
from books.models import Book


class ShelfFilter(django_filters.FilterSet):
    """Filter for the Shelf model."""

    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains', label="Name contains"
    )
    is_default = django_filters.BooleanFilter(
        field_name='is_default', label="Is default"
    )
    book_title = django_filters.CharFilter(
        field_name='shelfbook__book__title',
        lookup_expr='icontains',
        label="Book title contains")
    book_id = django_filters.NumberFilter(
        field_name='shelfbook__book__id', label="Book ID"
    )

    class Meta:
        """Meta options for ShelfFilter."""

        model = Shelf
        fields = ['name', 'is_default', 'book_title', 'book_id']
