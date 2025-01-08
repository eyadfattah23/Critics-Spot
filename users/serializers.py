#!/usr/bin/python3
"""Serializers for the users app."""

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from shelves.models import Shelf
from .models import CustomUser


class ShelfUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for Shelf model in user profile."""

    url = serializers.HyperlinkedIdentityField(
        view_name='shelf-detail',
        lookup_field='pk'
    )

    class Meta:
        """Meta options for ShelfUserProfileSerializer."""

        model = Shelf
        fields = ['id', 'name', 'url', 'image']


class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""

    shelves = ShelfUserProfileSerializer(many=True, read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        """Meta options for CustomUserSerializer."""

        model = CustomUser
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'date_joined', 'password',
                  'image', 'shelves']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""

    url = serializers.HyperlinkedIdentityField(
        view_name='user-details',
        lookup_field='pk'
    )

    class Meta:
        """Meta options for UserSerializer."""

        model = CustomUser
        fields = ['id', 'username', 'email', 'image', 'url']
        read_only_fields = ['email', 'image', 'id']


class UserUpdateSerializer(BaseUserSerializer):
    """Serializer for updating user details."""

    class Meta:
        """Meta options for UserUpdateSerializer."""

        model = CustomUser
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'image', 'bio']
        read_only_fields = ['email', 'id']


class UserProfileSerializer(BaseUserSerializer):
    """Serializer for user profile."""

    shelves = ShelfUserProfileSerializer(many=True, read_only=True)

    class Meta(BaseUserSerializer.Meta):
        """Meta options for UserProfileSerializer."""

        model = CustomUser
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name',
                  'date_joined', 'image',
                  'shelves', 'is_staff']
        read_only_fields = ['email', 'image', 'id']


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    """Serializer for creating a new user."""

    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    password_confirm = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    image = serializers.ImageField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta(BaseUserCreateSerializer.Meta):
        """Meta options for CustomUserCreateSerializer."""

        model = CustomUser
        fields = tuple(list(BaseUserCreateSerializer.Meta.fields) + [
            'password_confirm',
            'first_name',
            'last_name',
            'image'
        ])

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        # Remove password_confirm from attrs before parent validation
        attrs.pop('password_confirm', None)

        # Call parent validation
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        """Create the user using the parent class method."""
        user = super().create(validated_data)

        # Update additional fields
        if 'image' in validated_data:
            user.image = validated_data['image']
            user.save()

        return user
