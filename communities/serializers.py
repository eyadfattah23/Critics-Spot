#!/usr/bin/python3
from rest_framework import serializers
from .models import Community, Post, Comment
from users.models import CustomUser


class CustomCommunitySerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        view_name='user-details'
    )
    owner = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'members', 'image', 'owner']


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community-details'
    )

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community'
        ]


class CommunityPostCommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )

    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='community-posts'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'post']
