"""Permissions for the shelves app."""

from rest_framework.permissions import BasePermission
from .models import Shelf


class IsShelfOwnerOrAdmin(BasePermission):
    """Permission to check if the user is the owner of the shelf or an
    admin."""

    def has_object_permission(self, request, view, obj):
        """Check if the user has permission to access the object."""
        return ((request.user.is_authenticated) and (
            obj.user.id == request.user.id)) or (request.user.is_staff)


class IsShelvesOwnerOrAdmin(BasePermission):
    """Permission to check if the user is the owner of the shelves or an
    admin."""

    def has_permission(self, request, view):
        """Check if the user has permission to access the view."""
        return ((request.user.is_authenticated) and (request.user.is_staff)) or (
            int(view.kwargs['user_id']) == request.user.id)


class CanManageShelfBooks(BasePermission):
    """Custom permission to handle book operations on shelves."""

    def has_permission(self, request, view):
        """Check if the user has permission to manage books on the shelf."""
        # For adding/removing books, check if user owns the shelf
        shelf_id = view.kwargs.get('pk')
        try:
            shelf = Shelf.objects.get(pk=shelf_id)
            return request.user == shelf.user or request.user.is_staff
        except Shelf.DoesNotExist:
            return False
