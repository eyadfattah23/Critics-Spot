from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
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


class CustomUserViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['GET', 'PUT', 'PATCH', 'DELETE'])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserProfileSerializer(
                user, context={'request': request})
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=204)

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        kwargs['context'] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)


class CustomUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        return {'request': self.request}
