from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Community, Post, Comment, Like
from .serializers import (
    CustomCommunitySerializer, CustomCommunityDetailSerializer, CommunityCreateSerializer,
    PostSerializer, PostCreateSerializer, PostDetailsSerializer,
    CommunityPostCommentSerializer, CommunityPostCommentCreateSerializer,
    LikeSerializer, LikeCreateSerializer, CommunityUserSerializer,
    CommuntyCreateUserSerializer
)
from users.models import CustomUser


class CommunitiesList(generics.ListCreateAPIView):
    queryset = Community.objects.prefetch_related('members', 'owner', 'posts').all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityCreateSerializer
        return CustomCommunitySerializer


def perform_create(self, serializer):
    owner_id = self.request.data.get('owner')
    owner = get_object_or_404(CustomUser, pk=owner_id)
    serializer.save(owner=owner)


class CommunityDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomCommunityDetailSerializer
        return CommunityCreateSerializer


class CommunityPosts(generics.ListCreateAPIView):
    def get_queryset(self):
        return Post.objects.filter(community_id=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(community_id=self.kwargs['pk'])


class CommunityPostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailsSerializer
        return PostCreateSerializer


class CommunityPostComments(generics.ListCreateAPIView):
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityPostCommentCreateSerializer
        return CommunityPostCommentSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['pk'])


class CommunityPostCommentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommunityPostCommentSerializer
        return CommunityPostCommentCreateSerializer


class CommunityPostLikes(generics.ListCreateAPIView):
    def get_queryset(self):
        return Like.objects.filter(post_id=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LikeCreateSerializer
        return LikeSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['pk'])


class CommunityPostLikeDetails(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class ListMember(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommuntyCreateUserSerializer
        return CommunityUserSerializer

    def get_queryset(self):
        return Community.objects.get(pk=self.kwargs['pk']).members.all()

    def create(self, request, *args, **kwargs):
        community = get_object_or_404(Community, pk=self.kwargs['pk'])
        user_id = request.data.get('user')
        user = get_object_or_404(CustomUser, pk=user_id)
        if user in community.members.all():
            return Response({'error': 'User is already a member of the community.'}, status=400)
        community.members.add(user)
        return Response(status=201)


class RemoveMember(generics.CreateAPIView):
    serializer_class = CommuntyCreateUserSerializer

    def create(self, request, *args, **kwargs):
        community = get_object_or_404(Community, pk=self.kwargs['pk'])
        user = get_object_or_404(CustomUser, pk=request.data['user'])
        if user not in community.members.all():
            return Response({'error': 'User is not a member of the community.'}, status=400)
        community.members.remove(user)
        return Response(status=204)
