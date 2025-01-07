from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import CustomUser
from .serializers import *
from .filters import CustomUserFilter
from .permissions import *
# Create your views here.


class CustomUserViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsOwnerOrAdmin]

    def get_permissions(self):
        if self.action in ['create', 'activation', 'reset_password', 'reset_password_confirm']:
            return []  # No permissions needed for registration and activation
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return CustomUserCreateSerializer
        elif self.action == "me":
            return UserProfileSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return CustomUserSerializer

    @action(detail=False, methods=['GET', 'PUT', 'PATCH', 'DELETE'], permission_classes=[IsAuthenticated])
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
                partial=(request.method == 'PUT'),
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


class CustomUserDetails(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    serializer_class = CustomUserSerializer

    def get_serializer_context(self):
        return {'request': self.request}
