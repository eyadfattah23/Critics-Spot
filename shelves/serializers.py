from rest_framework import serializers
from users.models import CustomUser
from .models import Shelf, ShelfBook
from books.serializers import BookLightSerializer


class ShelfBookSerializer(serializers.ModelSerializer):
    book = BookLightSerializer()

    class Meta:
        model = ShelfBook
        fields = ['book', 'current_page']  # Include current_page


class ShelfSerializer(serializers.ModelSerializer):

    books = ShelfBookSerializer(
        source='shelfbook_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Shelf
        fields = ['id', 'name', 'is_default', 'books']


class ShelfCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        user = serializers.PrimaryKeyRelatedField(read_only=True)
        fields = ['name', 'user']
        extra_kwargs = {'user': {'read_only': True}}


class ShelfDeserializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['name', 'user']


class ShelfBookDeserializer(serializers.ModelSerializer):
    class Meta:
        model = ShelfBook
        fields = ['shelf', 'book', 'current_page']  # Include current_page
        extra_kwargs = {'shelf': {'read_only': True}}


'''

POST api/communities/<community_id>/join/

{
    "user": 1
}

community.members.add(user_id=1)

POST api/communities/<community_id>/leave
{
    "user": 1
}
community.members.delete(user_id=1)





'''
