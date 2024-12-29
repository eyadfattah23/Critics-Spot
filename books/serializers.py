#!/usr/bin/python3
'''
Book related serializers.
'''
from rest_framework import serializers
from .models import *


class BookLightSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        queryset=Author.objects.all(),
        view_name='author-details'
    )
    genres = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='genre-details',
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover', 'description',
                  'author', 'genres', 'publication_date', 'slug']


class BookDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'cover', 'description',
                  'author', 'genres', 'publication_date', 'buy_link', 'pages', 'author']


class VeryLightBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover', 'description']


class GenreLightSerializer(serializers.ModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='book-details',
    )

    class Meta:
        model = Genre
        fields = ['id', 'name', 'books']


class AuthorLightSerializer(serializers.ModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='book-details',
    )

    class Meta:
        model = Author
        fields = ['id', 'name', 'photo', 'bio', 'books']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(
        queryset=Author.objects.all(),
        view_name='author-details'
    )
    """ genres = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='genre-details',
    ) """
    genres = GenreLightSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'pages',
                  'author', 'cover', 'genres', 'avg_rating', 'description', 'publication_date', 'buy_link', 'added_date']


class GenreSerializer(serializers.ModelSerializer):
    books = VeryLightBookSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'books', 'added_date']


class AuthorSerializer(serializers.ModelSerializer):
    books = VeryLightBookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'birth_date',
                  'bio', 'death_date', 'books', 'photo']
        # read_only_fields = ['books']
