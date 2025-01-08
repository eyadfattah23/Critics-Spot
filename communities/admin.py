#!/usr/bin/python3
"""Admin configuration for the communities app."""
from django.utils.html import format_html, urlencode
from django.contrib import admin
from django.urls import reverse
from .models import Community, Post, Comment, Like
# Register your models here.


class CommunityPostInline(admin.TabularInline):
    """Inline admin for community posts."""

    model = Post


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    """Admin configuration for the Community model."""

    list_display = ['id', 'name', 'date_added', 'owner',
                    'number_of_members', 'number_of_posts', 'community_image']

    inlines = [CommunityPostInline]

    def number_of_members(self, obj):
        """Count the number of members in a community."""
        count = obj.members.count()
        url = (
            reverse('admin:users_customuser_changelist') + "?" +
            urlencode({'member_of_communities__id': str(obj.id)})
        )
        return format_html('<a href="{}">{}</a>', url, count)
    number_of_members.short_description = 'Number of Members'

    def number_of_posts(self, obj):
        """Count the number of posts in a community."""
        count = obj.posts.count()
        url = (
            reverse('admin:communities_post_changelist') + "?" +
            urlencode({'community__id': str(obj.id)})
        )
        return format_html('<a href="{}">{}</a>', url, count)
    number_of_posts.short_description = 'Number of Posts'

    def community_image(self, obj):
        """Display the community image."""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="border-radius: 5px;" />',
                obj.image.url
            )
        return "No Image"
    community_image.short_description = 'Image'

    search_fields = ['name', 'owner__username']
    list_select_related = ['owner']
    list_filter = ['owner', 'date_added']
    autocomplete_fields = ['owner']


class PostLikeInline(admin.TabularInline):
    """Inline admin for post likes."""

    model = Like


class PostCommentInline(admin.TabularInline):
    """Inline admin for post comments."""

    model = Comment
    list_display = ['user', 'content', 'created_at', 'post']
    list_select_related = ['user', 'post']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model."""

    list_display = ['id', 'user', 'created_at',
                    'content_beginning', 'community',
                    'number_of_likes', 'number_of_comments']
    list_select_related = ['user', 'community']
    inlines = [PostLikeInline, PostCommentInline]
    autocomplete_fields = ['user', 'community']
    search_fields = ['content', 'user__username']

    def content_beginning(self, post):
        """Get the beginning of the post content."""
        return "{}...".format(post.content[:30])
    content_beginning.short_description = 'Content'

    def number_of_likes(self, post):
        """Return the number of likes for the post."""
        return post.likes.count()
    number_of_likes.short_description = 'Number of Likes'

    def number_of_comments(self, post):
        """Return the number of comments for the post."""
        return post.comments.count()
    number_of_comments.short_description = 'Number of Comments'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin configuration for the Like model."""

    list_display = ['id', 'user', 'post', 'created_at']
    list_select_related = ['user', 'post']
    autocomplete_fields = ['user', 'post']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for the Comment model."""

    list_display = ['id', 'user', 'post', 'created_at']
    list_select_related = ['user', 'post']
    autocomplete_fields = ['user', 'post']
