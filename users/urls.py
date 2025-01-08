#!/usr/bin/python3
"""URL patterns for the users app."""
from django.urls import path, include
from rest_framework import routers

from . import views
from shelves.views import UserFavoritesList

router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/<pk>/favorites/',
        UserFavoritesList.as_view(),
        name='user-favorites'
    ),
]
