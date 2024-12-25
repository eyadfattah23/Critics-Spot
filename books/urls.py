from django.urls import path, include
from . import views


urlpatterns = [
    path('books/', views.books_list),
    path('books/<int:pk>', views.book_details, name='book-details'),

    path('authors/', views.authors_list),
    path('authors/<int:pk>', views.author_details, name='author-details'),

    path('genres/', views.genres_list),
    path('genres/<int:pk>', views.genre_details, name='genre-details'),
]
