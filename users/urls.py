from django.urls import path, include
from . import views


urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:id>', views.user_details),
]
