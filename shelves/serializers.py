from rest_framework import serializers
from users.models import CustomUser
from .models import Shelf, ShelfBook
from books.serializers import BookLightSerializer


class ShelfBookSerializer(serializers.ModelSerializer):
    book = BookLightSerializer()

    class Meta:
        model = ShelfBook
        fields = ['book']


class ShelfSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='user-details',
        lookup_field='pk'
    )
    books = ShelfBookSerializer(
        source='shelfbook_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Shelf
        fields = ['id', 'name', 'user', 'is_default', 'books']
