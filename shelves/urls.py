#!/usr/bin/python3
"""
URL patterns for the shelves app.
"""
from django.urls import path
from .views import ShelfList, UserShelfList, ShelfDetails, ShelfBookView

urlpatterns = [
    path('shelves/', ShelfList.as_view(), name='shelves-list'),
    path('users/<user_id>/shelves/',
         UserShelfList.as_view(), name='user-shelves-list'),

    path('shelves/<int:pk>/', ShelfDetails.as_view(), name='shelf-detail'),
    path('shelves/<int:pk>/books/<int:book_id>/',
         ShelfBookView.as_view(), name='book-to-shelf'),
    path('shelves/<int:pk>/books/',
         ShelfBookView.as_view(), name='book-to-shelf'),
]
