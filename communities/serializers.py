#!/usr/bin/python3
from rest_framework import serializers
from .models import Community
from users.models import CustomUser


class CustomCommunitySerializer(serializers.ModelSerializer):
    members = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        view_name='user-details'
    )
    owner = serializers.HyperlinkedRelatedField(
        queryset=CustomUser.objects.all(),
        view_name='owner-details'
    )

    class Meta:
        model = Community
        fields = ['id', 'name', 'description', 'members', 'image', 'owner']
