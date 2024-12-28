from django.urls import path, include
from . import views


urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:pk>/', views.user_details, name='user-details'),
]
