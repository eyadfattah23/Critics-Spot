#!usr/bin/python3
"""User and reviews related filters."""

from django_filters.rest_framework import FilterSet
from django_filters import filters, IsoDateTimeFilter
from .models import CustomUser, BookReview
from django.db import models as django_models


class CustomUserFilter(FilterSet):
    """Custom user filter."""

    class Meta:
        model = CustomUser
        fields = {
            'username': ['icontains'],
            'email': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'date_joined': ['gte', 'lte'],
        }
    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': IsoDateTimeFilter
        },

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
