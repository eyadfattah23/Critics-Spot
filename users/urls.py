from django.urls import path, include

from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetails.as_view(), name='user-details'),

]
