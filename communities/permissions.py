"""Permissions for the communities app."""
from rest_framework import permissions
from .models import Community


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Permission to allow only owner or admin to edit others can only read."""

    def has_object_permission(self, request, view, obj):
        """Check if the user has permission to access the object."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsCommunityOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to allow only community owners or admins to edit,
    others can only read.
    """

    def has_object_permission(self, request, view, obj):
        """Check if the user has permission to access the object."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff


class IsCommunityMemberForInteraction(permissions.BasePermission):
    """Permission to allow only community members to interact."""

    def has_permission(self, request, view):
        """Check if the user has permission to interact."""
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


class IsCommunityMember(permissions.BasePermission):
    """Custom permission to only allow members of a community to access it."""

    def has_object_permission(self, request, view, obj):
        """Check if the user is a member of the community."""
        return obj.members.filter(id=request.user.id).exists()
