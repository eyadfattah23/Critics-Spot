from rest_framework import serializers


class ShelfSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    user_id = serializers.IntegerField()
