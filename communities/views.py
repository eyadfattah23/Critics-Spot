from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Community, Post, Comment, Like
from .serializers import *


@api_view(['GET', 'POST'])
def communities_list(request):
    """ Return all the communities. """
    if request.method == 'POST':
        serializer = CustomCommunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=201)


    communities = Community.objects.prefetch_related('members', 'owner', 'posts').all()
    serializer = CustomCommunitySerializer(
        communities,
        many=True,
        context={'request': request}
    )
    return Response(serializer.data)


@api_view()
def community_details(request, pk):
    """Return the details of a specific community. """
    community = get_object_or_404(Community, pk=pk)
    serializer = CustomCommunitySerializer(
        community,
        context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def community_posts(request, pk):
    """Return the posts of a specific community. """
    community = get_object_or_404(Community, pk=pk)
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    posts = Post.objects.filter(community=community)
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def community_post_details(request, community_id, post_id):
    """Return the details of a specific post in a specific community."""
    community = get_object_or_404(Community, pk=community_id)
    post = get_object_or_404(Post, pk=post_id, community=community)
    serializer = PostDetailsSerializer(post, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def community_post_comments(request, pk):
    """Return the comments of a specific post in a specific community."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        serializer = CommunityPostCommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    comments = Comment.objects.filter(post=post)
    serializer = CommunityPostCommentSerializer(comments, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def community_post_likes(request, pk):
    """Return the likes of a specific post in a specific community."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        serializer = LikeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data, status=201)
    likes = Like.objects.filter(post=post)
    serializer = LikeSerializer(likes, many=True, context={'request': request})
    return Response(serializer.data)
