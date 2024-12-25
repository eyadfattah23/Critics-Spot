from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import *
from .serializers import *


def get_object_or_404(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise NotFound(f"{model.__name__} with ID {pk} not found.")

# Create your views here.


# Books

@api_view(['GET', 'POST'])
def books_list(request):
    if request.method == 'GET':
        books = Book.objects.select_related('author').all()
        serializer = BookLightSerializer(
            books, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        return Response('a new book has been created', status=201)


@api_view()
def book_details(request, pk):
    try:
        book = Book.objects.select_related(
            'author').prefetch_related('genres').get(pk=pk)
        serializer = BookSerializer(book, context={'request': request})
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)
    return Response(serializer.data)


""" @api_view()
def books_in_genre(request, genre_id):
    book = get_object_or_404(Book, id)
    serializer = BookSerializer(book)
    return Response(serializer.data)
 """

# Authors


@api_view()
def authors_list(request):
    authors = Author.objects.all()
    serializer = AuthorLightSerializer(
        authors, many=True, context={'request': request})
    return Response(serializer.data)


@api_view()
def author_details(request, pk):
    try:
        author = Author.objects.prefetch_related(
            'books').get(pk=pk)
        serializer = AuthorSerializer(author, context={'request': request})
    except Author.DoesNotExist:
        return Response({"error": "Author not found"}, status=404)
    return Response(serializer.data)


# Genres

@api_view()
def genre_details(request, pk):
    try:
        genre = Genre.objects.prefetch_related('books').get(pk=pk)
        serializer = GenreSerializer(genre, context={'request': request})
    except Genre.DoesNotExist:
        return Response({"error": "Genre not found"}, status=404)
    return Response(serializer.data)


@ api_view()
def genres_list(request):
    genres = Genre.objects.all()
    serializer = GenreLightSerializer(
        genres, many=True, context={'request': request})
    return Response(serializer.data)
