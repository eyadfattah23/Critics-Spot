from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Community


@receiver(post_save, sender=Community)
def add_owner_to_members(sender, instance, created, **kwargs):
    if created:  # Only for newly created communities
        instance.members.add(instance.owner)
