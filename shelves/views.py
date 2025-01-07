#!/usr/bin/python3
"""
Views for the shelves app.
"""
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from users.models import CustomUser
from .models import Shelf, ShelfBook
from .serializers import (
    ShelfSerializer, ShelfCreateSerializer,
    ShelfBookDeserializer, ShelfBookSerializer
)
from .filters import ShelfFilter
from .permissions import (
    IsShelvesOwnerOrAdmin,
    IsShelfOwnerOrAdmin, CanManageShelfBooks
)


class ShelfList(ListCreateAPIView):
    """
    A view for listing and creating shelves.
    """
    queryset = Shelf.objects.select_related(
        'user').prefetch_related('shelfbook_set__book').prefetch_related('shelfbook_set__book__author').all()
    serializer_class = ShelfSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ShelfFilter
    search_fields = ['name']
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        """
        Provide context to the serializer.
        """
        return {'request': self.request}


class UserShelfList(ListCreateAPIView):
    """
    A view for listing and creating shelves for a specific user.
    """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ShelfFilter
    search_fields = ['name']
    ordering_fields = ['shelfbook', 'name', 'shelfbook__book',
                       'shelfbook__date_added', 'shelfbook__date_finished']
    permission_classes = [IsShelvesOwnerOrAdmin]

    def get_queryset(self):
        """
        Return the queryset of shelves for the user.
        """
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, pk=user_id)
        return Shelf.objects.select_related('user').prefetch_related('shelfbook_set__book__genres').filter(user=user)

    def get_serializer_class(self):
        """
        Return the serializer class to be used for the request.
        """
        if self.request.method == 'POST':
            return ShelfCreateSerializer
        return ShelfSerializer

    def get_serializer_context(self):
        """
        Provide context to the serializer.
        """
        return {'request': self.request}

    def perform_create(self, serializer):
        """
        Save the new shelf instance.
        """
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, pk=user_id)
        serializer.save(user=user)


class ShelfDetails(RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting a shelf.
    """
    queryset = Shelf.objects.select_related(
        'user').prefetch_related('shelfbook_set__book').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsShelfOwnerOrAdmin]

    def get_serializer_class(self):
        """
        Return the serializer class to be used for the request.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return ShelfCreateSerializer
        return ShelfSerializer

    def get_serializer_context(self):
        """
        Provide context to the serializer.
        """
        return {'request': self.request}


class ShelfBookView(APIView):
    """
    A view for managing books on a shelf.
    """
    permission_classes = [IsAuthenticated, CanManageShelfBooks]

    def post(self, request, pk):
        """
        Add a book to the shelf.
        """
        shelf = get_object_or_404(
            Shelf.objects.prefetch_related('shelfbook_set__book'),
            pk=pk
        )
        data = request.data.copy()
        data['shelf'] = shelf.id
        serializer = ShelfBookDeserializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shelf=shelf)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, book_id):
        """
        Remove a book from the shelf.
        """
        shelf = get_object_or_404(Shelf, pk=pk)
        shelf_book = get_object_or_404(ShelfBook, shelf=shelf, book=book_id)
        shelf_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, book_id):
        """
        Update a book on the shelf.
        """
        shelf = get_object_or_404(Shelf, pk=pk)
        shelf_book = get_object_or_404(ShelfBook, shelf=shelf, book=book_id)
        serializer = ShelfBookDeserializer(
            shelf_book,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, pk, book_id=None):
        """
        Retrieve books on the shelf.
        """
        if book_id is None:
            shelf = get_object_or_404(
                Shelf.objects.prefetch_related('shelfbook_set__book'),
                pk=pk
            )
            serializer = ShelfSerializer(shelf, context={'request': request})
            return Response(serializer.data)
        else:
            shelf = get_object_or_404(Shelf, pk=pk)
            shelf_book = get_object_or_404(
                ShelfBook, shelf=shelf, book=book_id)
            serializer = ShelfBookSerializer(
                shelf_book, context={'request': request})
            return Response(serializer.data)


class UserFavoritesList(ListAPIView):
    """
    A view for listing a user's favorite books.
    """
    serializer_class = ShelfBookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return the queryset of favorite books for the user.
        """
        user_id = self.kwargs['pk']
        # Check if the user is requesting their own favorites or is staff
        if not (self.request.user.is_staff or self.request.user.id == int(user_id)):
            raise PermissionDenied("You can only view your own favorites")
        user = get_object_or_404(CustomUser, pk=user_id)
        favorites_shelf = get_object_or_404(Shelf, user=user, name='Favorites')
        return ShelfBook.objects.select_related(
            'book', 'book__author'
        ).prefetch_related(
            'book__genres'
        ).filter(shelf=favorites_shelf)
