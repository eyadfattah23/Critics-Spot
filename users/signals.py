#!/usr/bin/python3
"""Signals for users app."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from shelves.models import Shelf


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_default_shelves(sender, instance, created, **kwargs):
    """
    Create default shelves for a new user when they are created.

    Args:
        sender (class): The model class sending the signal.
        In this case, it's the User model.
        instance (User): The instance of the User model that
        triggered the signal.
        created (bool): A boolean indicating
        whether the User instance was created.
        kwargs (dict): Additional keyword arguments
        passed to the signal handler.

    Returns:
        None
    """
    if created:
        for shelf_name in Shelf.DEFAULT_SHELVES:
            Shelf.objects.create(
                name=shelf_name, user=instance, is_default=True)
