from users.models import CustomUser
from rest_framework import serializers
from .models import Community, Post, Comment, Like


class CommunityUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'image', 'username']


class CommuntyCreateUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())

    class Meta:
        model = Community
        fields = ['id', 'user']


class CustomCommunitySerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    owner = CommunityUserSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='community_details',
        lookup_field='pk'
    )

    def get_members_count(self, obj):
        return obj.members.count()

    class Meta:
        model = Community

        fields = ['id', 'name', 'description', 'members_count', 'image', 'owner', 'url']


class CommunityCreateSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())

    class Meta:
        model = Community
        fields = ['name', 'description', 'owner']


class PostSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community_details'
    )
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='community_post_details',
        lookup_field='pk'
    )

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community', 'likes_count', 'comments_count', 'url'
        ]

class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
    community = serializers.PrimaryKeyRelatedField(
        queryset=Community.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at',
                  'updated_at', 'user', 'community']


class CustomCommunityDetailSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    owner = CommunityUserSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='community_posts',
        lookup_field='pk'
    )

    def get_members_count(self, obj):
        return obj.members.count()

    class Meta:
        model = Community
        
        fields = ['id', 'name', 'description', 'members_count', 'image', 'owner', 'url']
        
        
class CommunityPostCommentSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    post = serializers.HyperlinkedRelatedField(
        queryset=Post.objects.all(),
        view_name='community_post_details'
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='community_post_comment_details',
        lookup_field='pk'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'post', 'url']


class CommunityPostCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ['content', 'user', 'post']


class CommunityPostCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

class CommentSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    url = serializers.HyperlinkedIdentityField(
        view_name='community_post_comment_details',
        lookup_field='pk'
    )

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'updated_at', 'user', 'url']


class LikeCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
    )
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
    )

    class Meta:
        model = Like
        fields = ['user', 'post']


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


class PostDetailsSerializer(serializers.ModelSerializer):
    user = CommunityUserSerializer()
    community = serializers.HyperlinkedRelatedField(
        queryset=Community.objects.all(),
        view_name='community_details'
    )
    likes = LikeSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'user',
            'community', 'likes', 'comments'
        ]
