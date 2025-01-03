from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .permissions import *
from .serializers import *


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'date_added']
    ordering = ['-date_added']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommunityCreateSerializer
        return CustomCommunitySerializer

    def perform_create(self, serializer):
        community = serializer.save(owner=self.request.user)
        community.members.add(self.request.user)

    def destroy(self, request, *args, **kwargs):
        community = self.get_object()
        if request.user != community.owner and not request.user.is_staff:
            raise PermissionDenied(
                "Only the owner or an admin can delete the community")
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        community = self.get_object()
        if request.user != community.owner and not request.user.is_staff:
            raise PermissionDenied(
                "Only the owner can update the community")
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        community = self.get_object()
        members = community.members.all()
        serializer = CommunityUserSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        community = self.get_object()
        if request.user in community.members.all():
            return Response(
                {'error': 'Already a member'},
                status=status.HTTP_400_BAD_REQUEST
            )
        community.members.add(request.user)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        community = self.get_object()
        if request.user == community.owner:
            return Response(
                {'error': 'Owner cannot leave the community'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user not in community.members.all():
            return Response(
                {'error': 'Not a member'},
                status=status.HTTP_400_BAD_REQUEST
            )
        community.members.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'])
    def delete(self, request, pk=None):
        community = self.get_object()
        if request.user != community.owner:
            raise PermissionDenied("Only the owner can delete the community")
        return super().delete(request, pk)


class CommunityPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsOwnerOrAdminOrReadOnly, IsCommunityMemberForInteraction]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'likes_count', 'comments_count']
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.filter(
            community_id=self.kwargs['community_pk']
        ).select_related(
            'user', 'community'
        ).prefetch_related(
            'likes', 'comments'
        ).annotate(
            likes_count=Count('likes'),
            comments_count=Count('comments')
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailsSerializer
        return PostSerializer

    def perform_create(self, serializer):
        community = get_object_or_404(
            Community, pk=self.kwargs['community_pk'])
        if self.request.user not in community.members.all():
            raise PermissionDenied("Only community members can create posts")
        serializer.save(user=self.request.user, community=community)

    @action(detail=True, methods=['post'])
    def like(self, request, community_pk=None, pk=None):
        post = self.get_object()
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response(
                {'error': 'Already liked'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Like.objects.create(user=request.user, post=post)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unlike(self, request, community_pk=None, pk=None):
        post = self.get_object()
        Like.objects.filter(user=request.user, post=post).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,
                          IsOwnerOrAdminOrReadOnly, IsCommunityMemberForInteraction]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['post_pk'],
            post__community_id=self.kwargs['community_pk']
        ).select_related('user', 'post')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommunityPostCommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post_pk'],
            community_id=self.kwargs['community_pk']
        )
        if self.request.user not in post.community.members.all():
            raise PermissionDenied("Only community members can comment")
        serializer.save(user=self.request.user, post=post)
