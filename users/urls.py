
from django.urls import path, include
from rest_framework import routers

from . import views
from shelves.views import UserFavoritesList
router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    # path('users/', views.CustomUserList.as_view()),
    # path('users/<int:pk>/', views.CustomUserDetails.as_view(), name='user-details'),
    path('', include(router.urls)),
    path('users/<user_id>/favorites/',
         UserFavoritesList.as_view(), name='user-favorites'),

]
