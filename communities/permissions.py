from rest_framework import permissions
from .models import Community


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsCommunityOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff


class IsCommunityMemberForInteraction(permissions.BasePermission):
    """
    Permission class to verify if user is a member of the community
    for create/update/delete operations, while allowing read access to all.
    """

    def has_permission(self, request, view):
        # Allow read operations for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write operations, check community membership
        community_pk = view.kwargs.get('community_pk')
        if not community_pk:
            return False

        return Community.objects.filter(
            id=community_pk,
            members=request.user
        ).exists()
