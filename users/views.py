#!/usr/bin/python3
"""Views for the users app."""

import requests
from django.http import HttpResponseRedirect
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import CustomUser
from .serializers import (
    CustomUserCreateSerializer,
    UserProfileSerializer, UserUpdateSerializer,
    CustomUserSerializer
)
from .permissions import IsOwnerOrAdmin


class CustomUserViewSet(DjoserUserViewSet):
    """Viewset for viewing and editing user instances."""
    
    queryset = CustomUser.objects.prefetch_related('shelves').all()
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsOwnerOrAdmin]

    def get_permissions(self):
        """Return the list of permissions that this view requires."""
        if self.action in [
            'create', 'activation',
            'reset_password', 'reset_password_confirm'
        ]:
            return []  # No permissions needed for registration and activation
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        """Return the serializer class to be used for the request."""
        if self.action == "create":
            return CustomUserCreateSerializer
        elif self.action == "me":
            return UserProfileSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return CustomUserSerializer

    @action(
        detail=False, methods=['GET', 'PUT', 'PATCH', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Handle the 'me' action for the user."""
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
        """Return the context for the serializer."""
        return {'request': self.request}


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user(request, uid, token):
    """Handle activation link from email."""
    try:
        # Build the activation endpoint URL
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        activation_url = f"{protocol}://{host}/auth/users/activation/"

        # Make the POST request
        response = requests.post(
            activation_url,
            json={
                'uid': uid,
                'token': token
            },
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 204:
            # Successful activation
            return Response({
                "detail": "Account activated successfully"
            }, status=status.HTTP_200_OK)
        else:
            # Failed activation
            return Response({
                "detail": "Activation failed. Invalid token or UID."
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "detail": f"Activation failed: {str(e)}"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def reset_password_confirm(request, uid, token):
    """Handle password reset confirmation link from email."""
    try:
        # Build the reset password endpoint URL
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host()
        reset_url = f"{protocol}://{host}/auth/users/reset_password_confirm/"

        # Make the POST request
        response = requests.post(
            reset_url,
            json={
                'uid': uid,
                'token': token,
                'new_password': 'your_new_password',
                're_new_password': 'your_new_password'
            },
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code == 204:
            # Redirect to frontend password reset page
            return HttpResponseRedirect(
                f'/reset-password/?uid={uid}&token={token}'
                )
        else:
            return Response({
                "detail": "Password reset failed. Invalid token or UID."
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "detail": f"Password reset failed: {str(e)}"
        }, status=status.HTTP_400_BAD_REQUEST)
