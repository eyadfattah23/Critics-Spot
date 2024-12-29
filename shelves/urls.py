from django.urls import path
from .views import *

urlpatterns = [
    path('shelves/', ShelfList.as_view(), name='shelves-list'),
    path('users/<user_id>/shelves/',
         UserShelfList.as_view(), name='user-shelves-list'),

    path('shelves/<int:pk>/', ShelfDetails.as_view(), name='shelf-details'),
    path('shelves/<int:pk>/books/<int:book_id>',
         book_to_shelf, name='book-to-shelf'),
    path('shelves/<int:pk>/books/',
         book_to_shelf, name='book-to-shelf'),
]
