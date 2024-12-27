from django.urls import path
from .views import shelves_list, shelf_details
import users.views

urlpatterns = [
    path('shelves/', shelves_list, name='shelves-list'),
    path('shelves/<int:pk>/', shelf_details, name='shelf-details'),
    path('users/<int:pk>/', users.views.user_details, name='user-details'),
]
