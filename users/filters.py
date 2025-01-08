#!usr/bin/python3
"""User and reviews related filters."""

from django_filters.rest_framework import FilterSet
from django_filters import IsoDateTimeFilter
from .models import CustomUser
from django.db import models as django_models


class CustomUserFilter(FilterSet):
    """Custom user filter."""

    class Meta:
        """Meta options for the CustomUserFilter class."""

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
