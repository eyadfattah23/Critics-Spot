#!/usr/bin/python3
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from books.models import Book
from shelves.models import Shelf
from .models import CustomUser

from books.serializers import BookLightSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    shelves = serializers.HyperlinkedRelatedField(
        queryset=Shelf.objects.select_related('user').all(),
        many=True,
        view_name='shelf-detail',
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='user-details',
        lookup_field='pk',
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'date_joined', 'image', 'shelves', 'url']


""" class UserCreateSerializer(serializers.ModelSerializer):
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
        return user """


class UserSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='user-details',
        lookup_field='pk'
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'image', 'url']

        read_only_fields = ['email', 'image', 'id']


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password', 'image', 'bio']
