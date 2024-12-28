from django.urls import path
from .views import *

urlpatterns = [
    path('shelves/', shelves_list, name='shelves-list'),
    path('users/<user_id>/shelves/', user_shelves_list, name='user-shelves-list'),

    path('shelves/<int:pk>/', shelf_details, name='shelf-details'),
    path('shelves/<int:pk>/books/<int:book_id>',
         book_to_shelf, name='book-to-shelf'),
    path('shelves/<int:pk>/books/',
         book_to_shelf, name='book-to-shelf'),
]
