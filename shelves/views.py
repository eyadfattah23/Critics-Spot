from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from .models import Shelf
from users.models import CustomUser
from .serializers import *
from .filters import *


class ShelfList(ListCreateAPIView):
    queryset = Shelf.objects.select_related(
        'user').prefetch_related('shelfbook_set__book').prefetch_related('shelfbook_set__book__author').all()
    serializer_class = ShelfSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ShelfFilter
    search_fields = ['name']

    def get_serializer_context(self):
        return {'request': self.request}


""" @api_view(['GET'])
def shelves_list(request):
    shelves = Shelf.objects.select_related(
        'user').prefetch_related('shelfbook_set__book').all()
    serializer = ShelfSerializer(
        shelves, many=True, context={'request': request})
    return Response(serializer.data)
 """


class UserShelfList(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ShelfFilter
    search_fields = ['name']

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, pk=user_id)
        return Shelf.objects.select_related('user').prefetch_related('shelfbook_set__book').filter(user=user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ShelfCreateSerializer
        return ShelfSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, pk=user_id)
        serializer.save(user=user)


class ShelfDetails(RetrieveUpdateDestroyAPIView):
    queryset = Shelf.objects.select_related(
        'user').prefetch_related('shelfbook_set__book').all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ShelfCreateSerializer
        return ShelfSerializer

    def get_serializer_context(self):
        return {'request': self.request}


""" @api_view(['GET', 'PUT', 'PATCH'])
def shelf_details(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk, user=request.user)

    if request.method == 'GET':
        serializer = ShelfSerializer(shelf, context={'request': request})
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ShelfCreateSerializer(
            shelf, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) """


@api_view(['POST', 'DELETE', 'PUT', 'PATCH'])
def book_to_shelf(request, pk, book_id=None):
    """Add a book to a shelf OR REMOVE it."""
    shelf = get_object_or_404(
        Shelf.objects.prefetch_related('shelfbook_set__book'), pk=pk)

    if request.method == 'POST' and not book_id:
        data = request.data.copy()
        data['shelf'] = shelf.id
        serializer = ShelfBookDeserializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(shelf=shelf)
        return Response(serializer.data, status=201)

    elif request.method == 'DELETE':
        shelf_book = get_object_or_404(
            ShelfBook, shelf=shelf, book=book_id)
        shelf_book.delete()
        return Response({"message": "Book removed from shelf"}, status=204)

    elif request.method in ['PUT', 'PATCH']:
        """
        PATCH /api/shelves/<shelf_id>/books/<book_id>/

        body: {"current_page": 100}
        """
        shelf_book = get_object_or_404(ShelfBook, shelf=shelf, book=book_id)
        partial = request.method == 'PATCH'
        serializer = ShelfBookDeserializer(
            shelf_book, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
