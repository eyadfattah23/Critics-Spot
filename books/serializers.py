#!/usr/bin/python3
'''
Book related serializers.
'''
from rest_framework import serializers
from .models import *
from users.models import *


class AuthorLightSerializer(serializers.ModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='book-details',
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='author-details',
        lookup_field='pk'
    )

    class Meta:
        model = Author
        fields = ['id', 'name', 'photo', 'bio', 'books', 'url']


class BookLightSerializer(serializers.ModelSerializer):
    author = AuthorLightSerializer()
    genres_names = serializers.SerializerMethodField()

    def get_genres_names(self, obj):
        return [genre.name for genre in obj.genres.all()]
    url = serializers.HyperlinkedIdentityField(
        view_name='book-details',
        lookup_field='pk'
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover', 'description',
                  'author', 'genres_names', 'publication_date', 'slug', 'url', 'avg_rating']
        read_only_fields = ['avg_rating']


class BookDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'cover', 'description',
                  'author', 'genres', 'publication_date', 'buy_link', 'pages', 'author']


class VeryLightBookSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='book-details',
        lookup_field='pk'
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover', 'description', 'url']


class GenreLightSerializer(serializers.ModelSerializer):
    books = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='book-details',
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='genre-details',
        lookup_field='pk'
    )

    class Meta:
        model = Genre
        fields = ['id', 'name', 'books', 'url']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorLightSerializer()
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


class BookReviewSerializer(serializers.ModelSerializer):
    book = serializers.HyperlinkedRelatedField(
        view_name='book-details',
        read_only=True,
    )

    class Meta:
        model = BookReview
        fields = ['id', 'book', 'rating', 'content', 'created_at', 'user']
