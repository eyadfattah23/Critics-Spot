from django.urls import path
from .views import shelves_list, shelf_details, create_shelf
import users.views

urlpatterns = [
    path('shelves/', shelves_list, name='shelves-list'),
    path('shelves/<int:pk>/', shelf_details, name='shelf-details'),
    path('shelves/create/<int:user_id>/', create_shelf, name='create-shelf'),
]
