from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Community, Post, Comment, Like
from .serializers import *
from users.models import CustomUser


class CommunityList(ListCreateAPIView):
    """ Return all the communities. """
    queryset = Community.objects.all()
    serializer_class = CustomCommunitySerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityDetail(RetrieveUpdateDestroyAPIView):
    """ Return the details of a specific community. """
    queryset = Community.objects.all()
    serializer_class = CustomCommunitySerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPost(ListCreateAPIView):
    """ Return the posts of a specific community. """
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostDetail(RetrieveUpdateDestroyAPIView):
    """ Return the details of a specific post in a specific community. """
    queryset = Post.objects.all()
    serializer_class = PostDetailsSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostComments(ListCreateAPIView):
    """Return the comments of a specific post in a specific community."""
    queryset = Comment.objects.all()
    serializer_class = CommunityPostCommentSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostCommentDetails(RetrieveUpdateDestroyAPIView):
    """Return the details of a specific comment in a specific post."""
    queryset = Comment.objects.all()
    serializer_class = CommunityPostCommentDetailsSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostLikes(ListCreateAPIView):
    """Return the likes of a specific post in a specific community."""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostLikeDetails(RetrieveUpdateDestroyAPIView):
    """Return the details of a specific like in a specific post."""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_serializer_context(self):
        return {'request': self.request}


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
