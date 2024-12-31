from django.urls import path, include

from . import views

urlpatterns = [
    path('users/', views.CustomUserList.as_view()),
    path('users/<int:pk>/', views.CustomUserDetails.as_view(), name='user-details'),
    path('users/<int:pk>/favorites/', views.user_favorites, name='user-favorites'),
    path('users/<int:pk>/favorites/<int:favorite_pk>/',
         views.favorite_detail, name='favorite-detail'),
    path('books/<int:pk>/reviews/',
         views.BookReviewsList.as_view(), name='book-reviews'),
    path('reviews/<int:pk>/', views.BookReviewDetails.as_view(),
         name='review-details'),
]
