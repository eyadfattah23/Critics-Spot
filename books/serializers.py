#!/usr/bin/python3
"""Book related serializers."""
from rest_framework import serializers
from .models import Book, Author, Genre, BookReview
from users.models import CustomUser


class AuthorLightSerializer(serializers.ModelSerializer):
    """Serializer for listing authors with light details."""

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
        """Meta class for AuthorLightSerializer."""

        model = Author
        fields = ['id', 'name', 'photo', 'bio', 'books', 'url']


class BookLightSerializer(serializers.ModelSerializer):
    """Serializer for listing books with light details."""

    author = AuthorLightSerializer()
    genres_names = serializers.SerializerMethodField()

    def get_genres_names(self, obj):
        """Get genre names for the book."""
        return [genre.name for genre in obj.genres.all()]
    url = serializers.HyperlinkedIdentityField(
        view_name='book-details',
        lookup_field='pk'
    )

    class Meta:
        """Meta class for BookLightSerializer."""

        model = Book
        fields = [
            'id',
            'title',
            'cover',
            'description',
            'author',
            'genres_names',
            'publication_date',
            'slug',
            'url',
            'avg_rating']
        read_only_fields = ['avg_rating']


class BookDeserializer(serializers.ModelSerializer):
    """Serializer for creating or updating book details."""

    class Meta:
        """Meta class for BookDeserializer."""

        model = Book
        fields = [
            'title',
            'cover',
            'description',
            'author',
            'genres',
            'publication_date',
            'buy_link',
            'pages',
            'author']


class GenreLightSerializer(serializers.ModelSerializer):
    """Serializer for listing genres with light details."""

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
        """Meta class for GenreLightSerializer."""

        model = Genre
        fields = ['id', 'name', 'books', 'url']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for retrieving detailed book information."""

    author = AuthorLightSerializer()
    genres = GenreLightSerializer(many=True)

    class Meta:
        """Meta class for BookSerializer."""

        model = Book
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for retrieving detailed genre information."""

    books = BookLightSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for GenreSerializer."""

        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for retrieving detailed author information."""

    books = BookLightSerializer(many=True, read_only=True)

    class Meta:
        """Meta class for AuthorSerializer."""

        fields = ['id', 'name', 'birth_date',
                  'bio', 'death_date', 'books', 'photo']


class UserReviewSerializer(serializers.ModelSerializer):
    """Serializer for user details in a review."""

    class Meta:
        """Meta class for UserReviewSerializer."""

        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'image']


class BookReviewSerializer(serializers.ModelSerializer):
    """Serializer for book reviews."""

    book = serializers.HyperlinkedRelatedField(
        view_name='book-details',
        read_only=True,
    )
    user = UserReviewSerializer(read_only=True)

    class Meta:
        """Meta class for BookReviewSerializer."""

        model = BookReview
        fields = ['id', 'book', 'rating', 'content', 'created_at', 'user']
