"""Signals for the communities app."""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Community, Post, Comment, Like


@receiver(post_save, sender=Community)
def add_owner_to_members(sender, instance, created, **kwargs):
    """Add the community owner to the members list after creation."""
    if created:
        instance.members.add(instance.owner)
