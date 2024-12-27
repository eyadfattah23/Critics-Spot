from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
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
        serializer = BookDeserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


'''
{
    "title": "The Lord of the Rings",
    "description": "A hobbit goes on an adventure",
    "author": 1,
    "genres": [1, 2],
    "publication_date": "1954-07-29",
    "buy_link": "https://www.google.com",
    "pages": 100
}

'''


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def book_details(request, pk):
    try:
        book = Book.objects.select_related(
            'author').prefetch_related('genres').get(pk=pk)

        if request.method == 'PUT' or request.method == 'PATCH':
            serializer = BookDeserializer(
                book, data=request.data, partial=request.method == 'PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'DELETE':
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=404)


""" @api_view()
def books_in_genre(request, genre_id):
    book = get_object_or_404(Book, id)
    serializer = BookSerializer(book)
    return Response(serializer.data)
 """

# Authors


@api_view(['GET', 'POST'])
def authors_list(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorLightSerializer(
            authors, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


'''
{
    "name": "J.R.R. Tolkien",
    "bio": "An English writer",
    "birth_date": "1892-01-03",
    "death_date": "1973-09-02"   
}
'''


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def author_details(request, pk):
    try:
        author = Author.objects.prefetch_related(
            'books').get(pk=pk)
        if request.method == 'PUT' or request.method == 'PATCH':
            serializer = AuthorSerializer(
                author, data=request.data, partial=request.method == 'PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            serializer = AuthorSerializer(author, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'DELETE':
            if author.books.count() > 0:
                return Response({"error": "Author has books"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    except Author.DoesNotExist:
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)


# Genres

@api_view(['GET', 'PUT', 'PATCH'])
def genre_details(request, pk):
    try:
        genre = Genre.objects.prefetch_related('books').get(pk=pk)
        if request.method == 'PUT' or request.method == 'PATCH':
            serializer = GenreSerializer(
                genre, data=request.data, partial=request.method == 'PATCH')
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'GET':
            serializer = GenreSerializer(genre, context={'request': request})
            return Response(serializer.data)
    except Genre.DoesNotExist:
        return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def genres_list(request):
    if request.method == 'GET':

        genres = Genre.objects.all()
        serializer = GenreLightSerializer(
            genres, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


'''
{
    "name": "Fantasy",
    "description": "A genre of speculative fiction set in a fictional universe, often inspired by real world myth and folklore."
}
'''
