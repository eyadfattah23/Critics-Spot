from rest_framework import serializers
from .models import Community, Post, Comment, Like
from users.models import CustomUser

class CustomCommunitySerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.select_related('community').all(),
        many=True,
        view_name='post-detail',
        lookup_field='pk'
    )
    members = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.prefetch_related('member_of_communities').all(),
        many=True,
        view_name='customuser-detail',
        lookup_field='pk'
    )
    owner = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.prefetch_related('communities').all(),
        view_name='customuser-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'members', 'image', 'owner', 'posts']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.prefetch_related('posts').all(),
        view_name='customuser-detail'
    )
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.prefetch_related('posts').all(),
        view_name='community-detail'
    )
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community', 'likes_count', 'comments_count'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

class CommunityPostCommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='customuser-detail'
    )
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='post-detail'
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='comment-detail'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'post', 'url']

class CommunityPostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='customuser-detail'
    )
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='post-detail'
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='like-detail'
    )

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at', 'url']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.prefetch_related('comments').all(),
        view_name='customuser-detail'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user']

class PostDetailsSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.prefetch_related('posts').all(),
        view_name='customuser-detail'
    )
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.prefetch_related('posts').all(),
        view_name='community-detail'
    )
    likes = serializers.HyperlinkedRelatedField(
        queryset=Like.objects.all(),
        many=True,
        view_name='like-detail',
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
        queryset=CustomUser.objects.prefetch_related('like_set').all(),  # Use the correct related name
        view_name='customuser-detail'
    )
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.prefetch_related('like_set').all(),  # Use the correct related name
        view_name='post-detail'
    )

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
