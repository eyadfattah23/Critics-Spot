#!/usr/bin/python3
"""
Views for the books app.
"""
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Book, Author, Genre, BookReview
from .serializers import (
    BookLightSerializer, BookDeserializer, BookSerializer,
    AuthorLightSerializer, AuthorSerializer,
    GenreLightSerializer, GenreSerializer, BookReviewSerializer
)
from .filters import BookFilter, AuthorFilter, GenreFilter, BookReviewFilter

# Books

class BookList(ListCreateAPIView):
    """
    API view to retrieve list of books or create a new book.

    get:
    Return a list of all the existing books.

    post:
    Create a new book instance.
    """
    queryset = Book.objects.select_related('author').prefetch_related(
        'author__books').prefetch_related('genres').all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description']
    ordering_fields = ['publication_date', 'avg_rating', 'pages', 'title']
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookDeserializer
        return BookLightSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get(self, request, *args, **kwargs):
        self.serializer_class = BookLightSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BookDeserializer
        return self.create(request, *args, **kwargs)


class BookDetails(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a book instance.

    get:
    Return the details of a specific book.

    put:
    Update the details of a specific book.

    patch:
    Partially update the details of a specific book.

    delete:
    Delete a specific book instance.
    """
    queryset = Book.objects.select_related(
        'author').prefetch_related('genres__books').all()
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookDeserializer
        return BookSerializer

    def get_serializer_context(self):
        return {'request': self.request}


# Authors

class AuthorList(ListCreateAPIView):
    """
    API view to retrieve list of authors or create a new author.

    get:
    Return a list of all the existing authors.

    post:
    Create a new author instance.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorLightSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter
    permission_classes = [DjangoModelPermissions]

    search_fields = ['name', 'bio']
    ordering_fields = ['name', 'birth_date', 'death_date']

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AuthorSerializer
        return AuthorLightSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = AuthorLightSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = AuthorSerializer
        return self.create(request, *args, **kwargs)


class AuthorDetails(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete an author instance.

    get:
    Return the details of a specific author.

    put:
    Update the details of a specific author.

    patch:
    Partially update the details of a specific author.

    delete:
    Delete a specific author instance.
    """
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_context(self):
        return {'request': self.request}


# Genres

class GenreList(ListCreateAPIView):
    """
    API view to retrieve list of genres or create a new genre.

    get:
    Return a list of all the existing genres.

    post:
    Create a new genre instance.
    """
    queryset = Genre.objects.prefetch_related('books').all()
    serializer_class = GenreLightSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = GenreFilter
    permission_classes = [DjangoModelPermissions]
    search_fields = ['name', 'description']
    ordering_fields = ['name']

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GenreSerializer
        return GenreLightSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = GenreLightSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = GenreSerializer
        return self.create(request, *args, **kwargs)


class GenreDetails(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a genre instance.

    get:
    Return the details of a specific genre.

    put:
    Update the details of a specific genre.

    patch:
    Partially update the details of a specific genre.

    delete:
    Delete a specific genre instance.
    """
    queryset = Genre.objects.prefetch_related('books').all()
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_context(self):
        return {'request': self.request}


# Book Reviews

class BookReviewsList(ListCreateAPIView):
    """
    API view to retrieve list of book reviews or create a new review for a specific book.

    get:
    Return a list of all the existing reviews for a specific book.

    post:
    Create a new review for a specific book.
    """
    serializer_class = BookReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookReviewFilter
    search_fields = ['content']
    ordering_fields = ['created_at', 'rating']

    def get_queryset(self):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, pk=book_id)
        return BookReview.objects.filter(book=book)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(book=book, user=self.request.user)


class BookReviewDetails(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a book review instance.

    get:
    Return the details of a specific book review.

    put:
    Update the details of a specific book review.

    patch:
    Partially update the details of a specific book review.

    delete:
    Delete a specific book review instance.
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response(
                {'error': 'You are not the author of this review'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().delete(request, *args, **kwargs)
