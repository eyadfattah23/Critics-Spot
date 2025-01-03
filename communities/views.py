from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch
from .models import Community, Post, Comment, Like
from .serializers import (
    CustomCommunitySerializer, CustomCommunityDetailSerializer,
    CommunityCreateSerializer,
    PostSerializer, PostCreateSerializer, PostDetailsSerializer,
    CommunityPostCommentSerializer, CommunityPostCommentCreateSerializer,
    LikeSerializer, LikeCreateSerializer, CommunityUserSerializer,
    CommuntyCreateUserSerializer, CommunityPostCommentUpdateSerializer
)
from users.models import CustomUser


class CommunitiesList(generics.ListCreateAPIView):

    # Optimize by adding posts__user to get post authors in a single query
    queryset = Community.objects.prefetch_related(
        'members',
        'owner',
        Prefetch('posts', queryset=Post.objects.select_related('user'))
    ).all()



    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityCreateSerializer
        return CustomCommunitySerializer

    def perform_create(self, serializer):
        owner_id = self.request.data.get('owner')
        owner = get_object_or_404(CustomUser, pk=owner_id)
        serializer.save(owner=owner)


class CommunityDetails(generics.RetrieveUpdateDestroyAPIView):
    # Add posts with their users to reduce queries
    queryset = Community.objects.prefetch_related(
        'members',
        Prefetch('posts', queryset=Post.objects.select_related('user')),
    ).select_related('owner')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomCommunityDetailSerializer
        return CommunityCreateSerializer


class CommunityPosts(generics.ListCreateAPIView):
    def get_queryset(self):
        return Post.objects.filter(community_id=self.kwargs['pk']).select_related(
            'user',
            'community'
        ).prefetch_related(
            'comments',
            'likes'
        ).annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True)
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(community_id=self.kwargs['pk'])


class CommunityPostDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.select_related(
        'user',
        'community'
    ).prefetch_related(
        Prefetch('comments', queryset=Comment.objects.select_related('user')),
        Prefetch('likes', queryset=Like.objects.select_related('user'))
    ).annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailsSerializer
        return PostCreateSerializer


class CommunityPostComments(generics.ListCreateAPIView):
    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['pk']
        ).select_related(
            'user',
            'post'
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityPostCommentCreateSerializer
        return CommunityPostCommentSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['pk'])


class CommunityPostCommentDetails(generics.RetrieveUpdateDestroyAPIView):

    queryset = Comment.objects.select_related(
        'post__user',  # Get post and its user in one join
        'post__community',  # Get community in the same query
        'user'
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommunityPostCommentSerializer
        return CommunityPostCommentUpdateSerializer


class CommunityPostLikes(generics.ListCreateAPIView):
    def get_queryset(self):
        return Like.objects.filter(
            post_id=self.kwargs['pk']
        ).select_related(
            'user',
            'post__user'  # Get post and its user in one join
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LikeCreateSerializer
        return LikeSerializer

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['pk'])


class CommunityPostLikeDetails(generics.RetrieveDestroyAPIView):
    queryset = Like.objects.select_related(
        'user',
        'post__user',  # Get post and its user in one join
        'post__community'  # Get community in the same query
    )
    serializer_class = LikeSerializer


class ListMember(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommuntyCreateUserSerializer
        return CommunityUserSerializer

    def get_queryset(self):
        # Cache the community query
        community = Community.objects.get(pk=self.kwargs['pk'])

        # Optimize the members query with a single efficient query
        return CustomUser.objects.filter(
            member_of_communities=community
        ).prefetch_related(
            Prefetch(
                'posts',
                queryset=Post.objects.filter(community=community)
            ),
            Prefetch(
                'comments',
                queryset=Comment.objects.filter(post__community=community)
            ),
            Prefetch(
                'likes',
                queryset=Like.objects.filter(post__community=community)
            )
        )

    def create(self, request, *args, **kwargs):
        community = get_object_or_404(Community, pk=self.kwargs['pk'])
        user_id = request.data.get('user')
        user = get_object_or_404(CustomUser, pk=user_id)

        # Optimize the membership check
        if community.members.filter(id=user.id).exists():
            return Response({'error': 'User is already a member of the community.'}, status=400)

        community.members.add(user)
        return Response(status=201)


class RemoveMember(generics.CreateAPIView):
    serializer_class = CommuntyCreateUserSerializer

    def create(self, request, *args, **kwargs):
        community = get_object_or_404(
            Community.objects.prefetch_related('members'),
            pk=self.kwargs['pk']
        )
        user = get_object_or_404(CustomUser, pk=request.data['user'])
        if user not in community.members.all():
            return Response({'error': 'User is not a member of the community.'}, status=400)
        community.members.remove(user)
        return Response(status=204)