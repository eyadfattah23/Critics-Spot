from users.models import CustomUser
from rest_framework import serializers
from .models import Community, Post, Comment, Like


class CommunityUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='users-detail',
        lookup_field='pk'
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'image', 'username', 'url']


class CustomCommunitySerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    owner = CommunityUserSerializer()

    def get_members_count(self, obj):
        return obj.members.count()

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'members_count', 'image', 'owner']


class PostSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community_details'
    )
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='community_post_details',
        lookup_field='pk'
    )

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community', 'likes', 'comments', 'url'
        ]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()


class CustomCommunityDetailSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    members_count = serializers.SerializerMethodField()
    members = CommunityUserSerializer(many=True)
    owner = CommunityUserSerializer()

    def get_members_count(self, obj):
        return obj.members.count()

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'members', 'posts', 'members_count', 'image', 'owner']


class CommunityPostCommentSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='community_post_details'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'post']


class CommentSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='community_post_comment_details',
        lookup_field='pk'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'url']


class PostDetailsSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community_details'
    )
    likes = serializers.HyperlinkedRelatedField(
        queryset=Like.objects.all(),
        many=True,
        view_name='community_post_like_details',
    )
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community', 'likes', 'comments'
        ]


class LikeSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='community_post_details'
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='community_post_like_details',
        lookup_field='pk'
    )

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at', 'url']
