#!/usr/bin/python3
"""URL patterns for the books app."""
from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the book list
    path('books/', views.BookList.as_view(), name='book-list'),
    # URL pattern for book details
    path('books/<int:pk>/', views.BookDetails.as_view(), name='book-details'),
    # URL pattern for book reviews
    path(
        'books/<int:pk>/reviews/',
        views.BookReviewsList.as_view(),
        name='book-reviews'),
    # URL pattern for review details
    path(
        'reviews/<int:pk>/',
        views.BookReviewDetails.as_view(),
        name='review-details'),

    # URL pattern for the author list
    path('authors/', views.AuthorList.as_view(), name='author-list'),
    # URL pattern for author details
    path(
        'authors/<int:pk>/',
        views.AuthorDetails.as_view(),
        name='author-details'),

    # URL pattern for the genre list
    path('genres/', views.GenreList.as_view(), name='genre-list'),
    # URL pattern for genre details
    path(
        'genres/<int:pk>/',
        views.GenreDetails.as_view(),
        name='genre-details'),
]
