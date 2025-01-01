from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Community, Post, Comment, Like
from .serializers import *

class CommunityViewSet(ModelViewSet):
    """Handle all community routes."""
    queryset = Community.objects.all().select_related('owner').prefetch_related('members', 'posts')
    serializer_class = CustomCommunitySerializer

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Return the posts of a specific community."""
        community = get_object_or_404(Community, pk=pk)
        posts = Post.objects.filter(community=community)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostViewSet(ModelViewSet):
    """Handle all post routes."""
    queryset = Post.objects.all().select_related('user', 'community').prefetch_related('likes', 'comments')
    serializer_class = PostSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Return the comments of a specific post."""
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommunityPostCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Return the likes of a specific post."""
        post = get_object_or_404(Post, pk=pk)
        likes = Like.objects.filter(post=post)
        serializer = CommunityPostLikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)

class CommentViewSet(ModelViewSet):
    """Handle all comment routes."""
    queryset = Comment.objects.all().select_related('user', 'post')
    serializer_class = CommunityPostCommentSerializer

class LikeViewSet(ModelViewSet):
    """Handle all like routes."""
    queryset = Like.objects.all().select_related('user', 'post')
    serializer_class = LikeSerializer
