#!/usr/bin/python3
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from shelves.models import Shelf
from .models import CustomUser


class ShelfUserProfileSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='shelf-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Shelf
        fields = ['id', 'name', 'url', 'image']


class CustomUserSerializer(serializers.ModelSerializer):
    shelves = ShelfUserProfileSerializer(many=True, read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'date_joined', 'password',
                  'image', 'shelves']


class UserSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='user-details',
        lookup_field='pk'
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'image', 'url']

        read_only_fields = ['email', 'image', 'id']


class UserUpdateSerializer(BaseUserSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'image', 'bio']
        read_only_fields = ['email', 'id']


"""     def update(self, instance, validated_data):
        # Remove password from validated_data if it wasn't provided
        if 'password' not in self.initial_data:
            validated_data.pop('password', None)
        return super().update(instance, validated_data)

    def validate_password(self, value):
        if value is None and self.instance:  # If updating and no password provided
            return self.instance.password  # Keep existing password
        return super().validate_password(value)
 """


class UserProfileSerializer(BaseUserSerializer):
    shelves = ShelfUserProfileSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'date_joined', 'image', 'shelves', 'is_staff']
        read_only_fields = ['email', 'image', 'id']


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
