# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from .filters import *
from .permissions import IsAdminOrReadOnly
# Create your views here.


# Books

class BookList(ListCreateAPIView):
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


class BookDetails(RetrieveUpdateDestroyAPIView):
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
    queryset = Author.objects.prefetch_related('books').all()
    serializer_class = AuthorSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_context(self):
        return {'request': self.request}


# Genres


class GenreList(ListCreateAPIView):
    queryset = Genre.objects.prefetch_related('books').all()
    serializer_class = GenreLightSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = GenreFilter
    search_fields = ['name', 'description']
    permission_classes = [DjangoModelPermissions]

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
    queryset = Genre.objects.prefetch_related('books').all()
    serializer_class = GenreSerializer
    permission_classes = [DjangoModelPermissions]

    def get_serializer_context(self):
        return {'request': self.request}


'''
{
    "name": "Fantasy",
    "description": "A genre of speculative fiction set in a fictional universe, often inspired by real world myth and folklore."
}
'''


class BookReviewsList(ListCreateAPIView):
    serializer_class = BookReviewSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookReviewFilter
    search_fields = ['content']
    ordering_fields = ['created_at', 'rating']
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, pk=book_id)
        return BookReview.objects.filter(book=book)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        book_id = self.kwargs['pk']
        book = get_object_or_404(Book, pk=book_id)
        serializer.save(book=book)


class BookReviewDetails(RetrieveUpdateDestroyAPIView):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer

    def get_serializer_context(self):
        return {'request': self.request}
