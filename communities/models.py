#!/usr/bin/python3
"""Groups related models."""
import os
from django.db import models
from django.conf import settings
from django.db.models import UniqueConstraint


class Post(models.Model):
    """Post model."""
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='posts')

    community = models.ForeignKey(
        'Community', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f"Post: {self.id} | Community: {self.community.id} by {self.user.username}: {self.user.id} at {self.created_at.ctime()}"


class Like(models.Model):
    """Like model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['post', 'user'],
                             name='unique_like_per_user_post')
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.post} on {self.created_at}"


class Comment(models.Model):
    """Comment model."""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='comments')

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.post}: {self.content[:30]}... ({self.created_at})"


def community_image_upload_to(instance, filename):
    """Generate file path for community images."""
    ext = filename.split('.')[-1]  # Get the file extension
    return os.path.join(f"community_images/{instance.name}/cover.{ext}")


class Community(models.Model):
    """Community model."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)  # Creator of the Community
    date_added = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='member_of_communities')  # users in each Community
    image = models.ImageField(
        upload_to=community_image_upload_to, default='default_community_image.jpeg')

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        # Save once to generate an ID for the instance
        if not self.id:
            super().save(*args, **kwargs)

        # Update the file path using the ID and save again if the file path needs an ID
        if self.image and f'communities_images/{self.name}' not in self.image.name:
            self.image.name = community_image_upload_to(self, self.image.name)
            super().save(*args, **kwargs)
