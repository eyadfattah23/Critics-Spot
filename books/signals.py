#!/usr/bin/python3
"""Signals for the b related models."""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import BookReview


@receiver([post_save, post_delete], sender=BookReview)
def update_avg_rating(sender, instance, **kwargs):
    """Signal to update avg_rating field on Book when a BookReview is created,
    updated, or deleted."""
    book = instance.book
    avg_rating = book.bookreview_set.aggregate(Avg('rating'))[
        'rating__avg'] or 0
    book.avg_rating = round(avg_rating, 2)  # Round to 2 decimal places
    book.save()
