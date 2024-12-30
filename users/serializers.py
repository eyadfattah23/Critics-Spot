#!/usr/bin/python3
from rest_framework import serializers
from .models import CustomUser, Favorite, BookReview
from shelves.models import Shelf
from books.models import Book
from books.serializers import BookLightSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    shelves = serializers.HyperlinkedRelatedField(
        queryset=Shelf.objects.all(),
        many=True,
        view_name='shelf-details',
    )
    favorites = serializers.HyperlinkedIdentityField(
        view_name='user-favorites',
        lookup_field='pk',
    )
    url = serializers.HyperlinkedIdentityField(
        view_name='user-details',
        lookup_field='pk',
    )
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'date_joined', 'image', 'shelves', 'favorites', 'url']


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

    book = BookLightSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'book']
        read_only_fields = ['user']



class UserSerializer(serializers.ModelSerializer):
    
    url = serializers.HyperlinkedIdentityField(
        view_name='user-details',
        lookup_field='pk'
    )
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'image', 'url']
        
        read_only_fields = [ 'email', 'image', 'id']
class BookReviewSerializer(serializers.ModelSerializer):
    book = serializers.HyperlinkedRelatedField(
        view_name='book-details',
        read_only=True,
    )
    class Meta:
        model = BookReview
        fields = ['id', 'book', 'rating', 'content', 'created_at', 'user']
