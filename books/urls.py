from django.urls import path, include
from . import views


urlpatterns = [
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetails.as_view(), name='book-details'),


    path('books/<int:pk>/reviews/',
         views.BookReviewsList.as_view(), name='book-reviews'),
    path('reviews/<int:pk>/', views.BookReviewDetails.as_view(),
         name='review-details'),

    path('authors/', views.AuthorList.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetails.as_view(), name='author-details'),

    path('genres/', views.GenreList.as_view(), name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetails.as_view(), name='genre-details'),
]
