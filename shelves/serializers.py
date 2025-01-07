#!/usr/bin/python3
"""
Serializers for the shelves app.
"""
from rest_framework import serializers
from .models import Shelf, ShelfBook
from books.serializers import BookLightSerializer


class ShelfBookSerializer(serializers.ModelSerializer):
    """
    Serializer for ShelfBook model.
    """
    book = BookLightSerializer()
    reading_progress = serializers.FloatField(read_only=True)

    class Meta:
        model = ShelfBook
        fields = ['book', 'current_page', 'notes',
                  'date_added', 'date_finished', 'reading_progress']


class ShelfSerializer(serializers.ModelSerializer):
    """
    Serializer for Shelf model.
    """
    books = ShelfBookSerializer(
        source='shelfbook_set',
        many=True,
        read_only=True
    )
    book_count = serializers.IntegerField(
        source='shelfbook_set.count',
        read_only=True
    )

    class Meta:
        model = Shelf
        fields = ['id', 'name', 'user', 'is_default',
                  'books', 'book_count', 'url', 'image']


class ShelfCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Shelf.
    """
    class Meta:
        model = Shelf
        user = serializers.PrimaryKeyRelatedField(read_only=True)
        fields = ['name', 'user', 'image']
        extra_kwargs = {'user': {'read_only': True}}


class ShelfDeserializer(serializers.ModelSerializer):
    """
    Deserializer for Shelf model.
    """
    class Meta:
        model = Shelf
        fields = ['name', 'user', 'image']


class ShelfBookDeserializer(serializers.ModelSerializer):
    """
    Deserializer for ShelfBook model.
    """
    class Meta:
        model = ShelfBook
        fields = ['shelf', 'book', 'current_page', 'date_finished']
        extra_kwargs = {'shelf': {'read_only': True}}
