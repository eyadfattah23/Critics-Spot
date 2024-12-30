from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Community, Post, Comment, Like
from .serializers import *
from users.models import CustomUser


class CommunityViewSet(ModelViewSet):
    """ Handels all communities' routes. """
    queryset = Community.objects.all()
    serializer_class = CustomCommunitySerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostViewSet(ModelViewSet):
    """ Handels all the routes posts of a specific community. """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostCommentsViewSet(ModelViewSet):
    """ Handels all the routes comments of a specific post in a specific community. """
    queryset = Comment.objects.all()
    serializer_class = CommunityPostCommentSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommunityPostLikesViewSet(ModelViewSet):
    """ Handels all the routes likes of a specific post in a specific community. """
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
