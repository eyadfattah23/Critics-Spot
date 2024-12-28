from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Shelf
from users.models import CustomUser
from .serializers import *


@api_view(['GET'])
def shelves_list(request):
    """ Return all the shelves. """
    shelves = Shelf.objects.select_related(
        'user').prefetch_related('shelfbook_set__book').all()
    serializer = ShelfSerializer(
        shelves, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def user_shelves_list(request, user_id):
    """ Return the users shelves from the id of the user. """
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'GET':
        shelves = Shelf.objects.select_related(
            'user').prefetch_related('shelfbook_set__book').filter(user=user)
        serializer = ShelfSerializer(
            shelves, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = user.id
        serializer = ShelfCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=201)


@api_view(['GET', 'PUT', 'PATCH'])
def shelf_details(request, pk):
    """Return or update the details of a shelf."""
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
        return Response(serializer.data)


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
