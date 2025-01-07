from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Shelf


class IsShelfOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return ((request.user.is_authenticated) and (
            obj.user.id == request.user.id)) \
            or (request.user.is_staff)


class IsShelvesOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return ((request.user.is_authenticated) and (request.user.is_staff)) \
            or (int(view.kwargs['user_id']) == int(request.user.id))


class CanManageShelfBooks(BasePermission):
    """
    Custom permission to handle book operations on shelves.
    """

    def has_permission(self, request, view):
        # For adding/removing books, check if user owns the shelf
        shelf_id = view.kwargs.get('pk')
        try:
            shelf = Shelf.objects.get(pk=shelf_id)
            return request.user == shelf.user or request.user.is_staff
        except Shelf.DoesNotExist:
            return False
