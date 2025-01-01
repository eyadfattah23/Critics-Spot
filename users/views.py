from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import CustomUser
from .serializers import *
from .filters import CustomUserFilter
# Create your views here.


class CustomUserList(ListCreateAPIView):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CustomUserFilter
    search_fields = ['username', 'first_name', 'last_name', 'email']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return CustomUserSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get(self, request, *args, **kwargs):
        self.serializer_class = CustomUserSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        return self.create(request, *args, **kwargs)


class CustomUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        return {'request': self.request}
