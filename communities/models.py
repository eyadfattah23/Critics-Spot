#!/usr/bin/python3
"""Models for the communities app."""
import os
from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint


class Post(models.Model):
    """Model representing a post in a community."""

    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts')

    community = models.ForeignKey(
        'Community', on_delete=models.CASCADE, related_name='posts'
    )

    def __str__(self):
        """Return a string representation of the post."""
        return (
            f"Post: {self.id} | Community: {self.community.id} by "
            f"{self.user.username}: {self.user.id} at {self.created_at.ctime()}"
        )


class Like(models.Model):
    """Model representing a like on a post."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Like model."""

        constraints = [
            UniqueConstraint(
                fields=[
                    'post',
                    'user'],
                name='unique_like_per_user_post')]
        indexes = [
            models.Index(fields=['user', 'post']),
        ]

    def __str__(self):
        """Return a string representation of the like."""
        return f"{self.user.username} liked {self.post} on {self.created_at}"


class Comment(models.Model):
    """Model representing a comment on a post."""

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the comment."""
        return (
            f"{self.user.username} commented on {self.post}: "
            f"{self.content[:30]}... ({self.created_at})"
        )


def community_image_upload_to(instance, filename):
    """Generate file path for community images."""
    ext = filename.split('.')[-1]  # Get the file extension
    return os.path.join(f"community_images/{instance.name}/cover.{ext}")


class Community(models.Model):
    """Model representing a community."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='communities')  # Creator of the Community
    date_added = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='member_of_communities')  # users in each Community
    image = models.ImageField(
        upload_to=community_image_upload_to,
        default='default_community_image.jpeg')

    def __str__(self):
        """Return a string representation of the community."""
        return f"{self.name}"
