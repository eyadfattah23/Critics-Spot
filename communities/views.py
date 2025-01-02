from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Community, Post, Comment, Like
from .serializers import *
from users.models import CustomUser

class CommunitiesList(APIView):
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


class CommunityDetails(APIView):
    """Return the details of a specific community. """
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CustomCommunityDetailSerializer(
            community,
            context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = CustomCommunitySerializer(
            community,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        community.delete()
        return Response(status=204)


class CommunityPosts(APIView):
    """Return the posts of a specific community. """
    def get(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        posts = Post.objects.filter(community=community)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        serializer = PostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class CommunityPostDetails(APIView):
    """Return the details of a specific post in a specific community."""
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailsSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailsSerializer(
            post,
            data=request.data,
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=204)


class CommunityPostComments(APIView):
    """Return the comments of a specific post in a specific community."""
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommunityPostCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommunityPostCommentCreateSerializer(data=request.data, context={'request': request})
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
            context={'request': request},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        return self.put(request, pk)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=204)


class CommunityPostLikes(APIView):
    """Return the likes of a specific post in a specific community."""
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        likes = Like.objects.filter(post=post)
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = LikeCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        user = CustomUser.objects.get(id=request.user)
        new_like = Like.objects.create(user=user, post=post)
        post.likes.add(new_like)
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


class AddMember(APIView):
    """Add a member to a specific community."""
    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        user = get_object_or_404(CustomUser, pk=request.data['user_id'])
        if user in community.members.all():
            return Response({'error': 'User is already a member of the community.'}, status=400)
        community.members.add(user)
        return Response(status=201)


class RemoveMember(APIView):
    """Remove a member from a specific community."""
    def post(self, request, pk):
        community = get_object_or_404(Community, pk=pk)
        user = get_object_or_404(CustomUser, pk=request.data['user_id'])
        if user not in community.members.all():
            return Response({'error': 'User is not a member of the community.'}, status=400)
        community.members.remove(user)
        return Response(status=204)
