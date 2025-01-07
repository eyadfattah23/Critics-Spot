#!/usr/bin/python3
"""
Permissions for the books app.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed for any request.
    """
    def has_permission(self, request, view):
        """
        Check if the request has permission to proceed.
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
