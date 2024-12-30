from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Community, Post, Comment, Like
from .serializers import *
from users.models import CustomUser


class CommunityViewSet(ModelViewSet):
    """ Handels all communities' routes. """
    queryset = Community.objects.all().select_related('owner').prefetch_related('members', 'posts')
    serializer_class = CustomCommunitySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostViewSet(ModelViewSet):
    """ Handels all the routes posts of a specific community. """
    queryset = Post.objects.all().select_related('user', 'community').prefetch_related('likes', 'comments')
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['updated_at']

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostCommentsViewSet(ModelViewSet):
    """ Handels all the routes comments of a specific post in a specific community. """
    queryset = Comment.objects.all().select_related('user', 'post')
    serializer_class = CommunityPostCommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['updated_at']
    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostLikesViewSet(ModelViewSet):
    """ Handels all the routes likes of a specific post in a specific community. """
    queryset = Like.objects.all().select_related('user', 'post')
    serializer_class = LikeSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityMemberList(APIView):
    """Return all the members of a specific community."""
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
