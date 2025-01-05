from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        # For list action - only admins can see all users
        if view.action == 'list':
            return request.user.is_staff
        # For create/register - anyone can create a new user
        if view.action == 'register':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow access if:
        # 1. User is admin, or
        # 2. User is accessing their own data
        return request.user.is_staff or obj.id == request.user.id
