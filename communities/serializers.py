#!/usr/bin/python3
"""Serializers for the communities app."""
from rest_framework import serializers
from users.models import CustomUser
from .models import Community, Post, Comment, Like


class CommunityUserSerializer(serializers.ModelSerializer):
    """Serializer for user details in a community."""

    class Meta:
        """Meta options for the CommunityUserSerializer."""

        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'image']


class CommunityCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new community."""

    class Meta:
        """Meta options for the CommunityCreateSerializer."""

        model = Community
        fields = ['name', 'description', 'image']


class CustomCommunitySerializer(serializers.ModelSerializer):
    """Serializer for retrieving detailed community information."""

    owner = CommunityUserSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        """Meta options for the CustomCommunitySerializer."""

        model = Community
        fields = [
            'id', 'name', 'description', 'image', 'owner',
            'members_count', 'posts_count', 'date_added', 'is_member'
        ]

    def get_members_count(self, obj):
        """Return the number of members in the community."""
        return obj.members.count()

    def get_posts_count(self, obj):
        """Return the number of posts in the community."""
        return obj.posts.count()

    def get_is_member(self, obj):
        """Check if the user is a member of the community."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(id=request.user.id).exists()
        return False


class PostSerializer(serializers.ModelSerializer):
    """Serializer for community posts."""

    user = CommunityUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        """Meta options for the PostSerializer."""

        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at',
            'user', 'community', 'likes_count', 'comments_count',
            'is_liked'
        ]
        read_only_fields = ['user', 'community']

    def get_likes_count(self, obj):
        """Return the number of likes for the post."""
        return obj.likes.count()

    def get_comments_count(self, obj):
        """Return the number of comments for the post."""
        return obj.comments.count()

    def get_is_liked(self, obj):
        """Check if the user has liked the post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostDetailsSerializer(PostSerializer):
    """Serializer for detailed post information including comments."""

    comments = serializers.SerializerMethodField()

    class Meta(PostSerializer.Meta):
        """Meta options for the PostDetailsSerializer."""

        fields = PostSerializer.Meta.fields + ['comments']

    def get_comments(self, obj):
        """Return the comments for the post."""
        comments = obj.comments.select_related('user').order_by('-created_at')
        return CommentSerializer(
            comments, many=True, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments on posts."""

    user = CommunityUserSerializer(read_only=True)

    class Meta:
        """Meta options for the CommentSerializer."""

        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user']
        read_only_fields = ['user']


class CommunityPostCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new comment on a post."""

    class Meta:
        """Meta options for the CommunityPostCommentCreateSerializer."""

        model = Comment
        fields = ['content']


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for likes on posts."""

    user = CommunityUserSerializer(read_only=True)

    class Meta:
        """Meta options for the LikeSerializer."""

        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user']
