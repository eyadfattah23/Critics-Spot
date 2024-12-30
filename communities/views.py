from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import APIView
from .models import Community, Post, Comment, Like
from .serializers import *
from users.models import CustomUser


class CommunityList(APIView):
    """ Return all the communities. """
    def get(self, request):
        communities = Community.objects.prefetch_related('members', 'owner', 'posts').all()
        serializer = CustomCommunitySerializer(
            communities,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomCommunitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=201)


class CommunityDetail(APIView):
    """ Return the details of a specific community. """
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CustomCommunitySerializer(community, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CustomCommunitySerializer(community, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CustomCommunitySerializer(community, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        community.delete()
        return Response(status=204)


class CommunityPost(APIView):
    """ Return the posts of a specific community. """
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        posts = Post.objects.filter(community=community)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(community=community)
        return Response(serializer.data, status=201)


class CommunityPostDetail(APIView):
    """ Return the details of a specific post in a specific community. """
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailsSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailsSerializer(post, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailsSerializer(post, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=204)


class CommunityPostComments(APIView):
    """Return the comments of a specific post in a specific community."""
    def get(self, request, pk):
        comments = Comment.objects.filter(post=post)
        serializer = CommunityPostCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CommunityPostCommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class CommunityPostCommentDetails(APIView):
    """Return the details of a specific comment in a specific post."""
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommunityPostCommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommunityPostCommentSerializer(
            comment,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommunityPostCommentSerializer(
            comment,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=204)


class CommunityPostLikes(APIView):
    """Return the likes of a specific post in a specific community."""
    def get(self, request, pk):
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = LikeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class CommunityPostLikeDetails(APIView):
    """Return the details of a specific like in a specific post."""
    def get(self, request, pk):
        like = get_object_or_404(Like, pk=pk)
        serializer = LikeSerializer(like, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        like = get_object_or_404(Like, pk=pk)
        like.delete()
        return Response(status=204)


class CommunityMemberList(APIView):
    """Return all the members of a specific community."""
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        members = community.members.all()
        serializer = CustomUserSerializer(members, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        """Add or remove a member from a specific community."""
        community = get_object_or_404(Community, pk=pk)
        user = get_object_or_404(CustomUser, pk=request.data['user_id'])
        if 'join' in request.path:
            if user in community.members.all():
                return Response({'error': 'User is already a member of the community.'}, status=400)
            community.members.add(user)
            return Response(status=201)
        elif 'leave' in request.path:
            if user not in community.members.all():
                return Response({'error': 'User is not a member of the community.'}, status=400)
            community.members.remove(user)
            return Response(status=204)
