#!/usr/bin/python3
"""Groups related models."""
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

    def __str__(self):
        return f"Post by {self.user.username} at {self.created_at}"


class Like(models.Model):
    """Like model."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
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


class Group(models.Model):
    """Group model."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000)
    posts = models.ManyToManyField(Post, related_name='groups')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)  # Creator of the group
    date_added = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='groups')  # users in each group

    def __str__(self):
        return f"{self.name} group, owned by {self.user.username} created at {self.date_added}"
