from rest_framework import serializers
from .models import Community, Post, Comment, Like
from users.models import CustomUser
from users.serializers import CustomUserSerializer

class CustomCommunitySerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        many=True,
        view_name='communitypost-detail',
        lookup_field='pk'
    )
    members = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        view_name='user-details',
        lookup_field='pk'
    )
    owner = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details',
        lookup_field='pk'
    )

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'members', 'image', 'owner', 'posts']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community-detail'
    )
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community', 'likes', 'comments'
        ]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()

class CommunityPostCommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='communitypost-detail'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'post']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user']

class PostDetailsSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community-detail'
    )
    likes = serializers.HyperlinkedRelatedField(
        queryset=Like.objects.all(),
        many=True,
        view_name='communitypostlike-detail',
    )
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community', 'likes', 'comments'
        ]

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details'
    )
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='communitypost-detail'
    )

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
