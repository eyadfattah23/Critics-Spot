from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
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


class UserShelfList(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ShelfFilter
    search_fields = ['name']
    ordering_fields = ['shelfbook', 'name', 'shelfbook__book',
                       'shelfbook__date_added', 'shelfbook__date_finished',
                       ]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, pk=user_id)
        return Shelf.objects.select_related('user').prefetch_related('shelfbook_set__book__genres').filter(user=user)

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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ShelfCreateSerializer
        return ShelfSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ShelfBookView(APIView):
    def post(self, request, pk):
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
        shelf = get_object_or_404(Shelf, pk=pk)
        shelf_book = get_object_or_404(ShelfBook, shelf=shelf, book=book_id)
        shelf_book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk, book_id):
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

        """
        PATCH /api/shelves/<shelf_id>/books/<book_id>/

        body: {"current_page": 100}
        """


class UserFavoritesList(ListAPIView):
    serializer_class = ShelfBookSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(CustomUser, pk=user_id)
        # Get the Favorites shelf and its books
        favorites_shelf = get_object_or_404(Shelf, user=user, name='Favorites')
        return ShelfBook.objects.select_related(
            'book', 'book__author'
        ).prefetch_related(
            'book__genres'
        ).filter(shelf=favorites_shelf)
