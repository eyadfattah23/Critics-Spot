#!/usr/bin/python3
"""Permissions for the users app."""

from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed for any request.
    """

    def has_permission(self, request, view):
        """Check if the request has permission to proceed."""
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """Custom permission to only allow owners or admins to access objects."""

    def has_permission(self, request, view):
        """Check if the request has permission to proceed."""
        # For list action - only admins can see all users
        if view.action == 'list':
            return request.user.is_staff
        # For create/register - anyone can create a new user
        if view.action == 'register':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Check if the request has object-level permission to proceed."""
        # Only allow access if:
        # 1. User is admin, or
        # 2. User is accessing their own data
        return request.user.is_staff or obj.id == request.user.id
