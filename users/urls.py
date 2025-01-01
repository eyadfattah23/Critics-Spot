from django.urls import path, include

from . import views
from shelves.views import UserFavoritesList
urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetails.as_view(), name='user-details'),
    path('users/<user_id>/favorites/',
         UserFavoritesList.as_view(), name='user-favorites'),
]
