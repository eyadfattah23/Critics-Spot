from django.urls import path, include
from . import views 

urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:pk>', views.user_details, name='user-details'),
    path('users/<int:pk>/favorites/', views.user_favorites, name='user-favorites'),
    path('users/<int:pk>/favorites/<int:favorite_pk>', views.favorite_detail, name='favorite-detail')
]
