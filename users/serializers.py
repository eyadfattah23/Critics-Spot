#!/usr/bin/python3
from rest_framework import serializers
from .models import CustomUser, Favorite
from shelves.models import Shelf
from books.models import Book


class CustomUserSerializer(serializers.ModelSerializer):
    shelves = serializers.HyperlinkedRelatedField(
        queryset=Shelf.objects.all(),
        many=True,
        view_name='shelf-details',
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'date_joined', 'image', 'shelves']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio', 'image']
        # Hide the password when sending the data
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            # if no bio provided the get method will return an empty string
            bio=validated_data.get('bio', ''),
            # if no image provided the get method will return the default image
            image=validated_data.get('image', 'default_user_image.png')
        )
        return user


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details',
    )

    book = serializers.HyperlinkedRelatedField(
        queryset=Book.objects.all(),
        view_name='book-details',
    )

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'book']
        read_only_fields = ['user']
