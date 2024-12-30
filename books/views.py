# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .filters import *
# Create your views here.


# Books

class BookList(ListCreateAPIView):
    queryset = Book.objects.select_related(
        'author').prefetch_related('genres').all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

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
        'author').prefetch_related('genres').all()

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuthorFilter

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

    def get_serializer_context(self):
        return {'request': self.request}


# Genres


class GenreList(ListCreateAPIView):
    queryset = Genre.objects.prefetch_related('books').all()
    serializer_class = GenreLightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GenreFilter

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

    def get_serializer_context(self):
        return {'request': self.request}


'''
{
    "name": "Fantasy",
    "description": "A genre of speculative fiction set in a fictional universe, often inspired by real world myth and folklore."
}
'''
