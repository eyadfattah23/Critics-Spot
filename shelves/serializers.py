from rest_framework import serializers
from users.models import CustomUser
from .models import Shelf, ShelfBook
from books.serializers import BookLightSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']


class ShelfSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details',
        lookup_field='pk'
    )
    books = BookLightSerializer(many=True, read_only=True)

    class Meta:
        model = Shelf
        fields = ['id', 'name', 'user', 'is_default', 'books']


class ShelfBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelfBook
        fields = ['shelf', 'book']