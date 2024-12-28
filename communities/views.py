from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Community, Post, Comment, Like
from .serializers import *
from users.models import CustomUser

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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def community_details(request, pk):
    """Return the details of a specific community. """
    community = get_object_or_404(Community, pk=pk)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = CustomCommunitySerializer(
            community,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    elif request.method == 'DELETE':
        community.delete()
        return Response(status=204)
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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def community_post_details(request, pk):
    """Return the details of a specific post in a specific community."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = PostDetailsSerializer(
            post,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=204)
    post = get_object_or_404(Post, pk=pk)
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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def community_post_comment_details(request, pk):
    """Return the details of a specific comment in a specific post."""
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = CommunityPostCommentSerializer(
            comment,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=204)
    serializer = CommunityPostCommentSerializer(comment, context={'request': request})
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


@api_view(['GET', 'DELETE'])
def community_post_like_details(request, pk):
    """Return the details of a specific like in a specific post."""
    like = get_object_or_404(Like, pk=pk)
    if request.method == 'DELETE':
        like.delete()
        return Response(status=204)
    serializer = LikeSerializer(like, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
def add_member(request, pk):
    """Add a member to a specific community."""
    community = get_object_or_404(Community, pk=pk)
    user = get_object_or_404(CustomUser, pk=request.data['user_id'])
    if user in community.members.all():
        return Response({'error': 'User is already a member of the community.'}, status=400)
    community.members.add(user)
    return Response(status=201)


@api_view(['POST'])
def remove_member(request, pk):
    """Remove a member from a specific community."""
    community = get_object_or_404(Community, pk=pk)
    user = get_object_or_404(CustomUser, pk=request.data['user_id'])
    if user not in community.members.all():
        return Response({'error': 'User is not a member of the community.'}, status=400)
    community.members.remove(user)
    return Response(status=204)
