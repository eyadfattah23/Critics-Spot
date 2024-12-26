from django.urls import path
from .views import shelves_list, shelf_details, user_details

urlpatterns = [
    path('shelves/', shelves_list, name='shelves-list'),
    path('shelves/<int:id>/', shelf_details, name='shelf-details'),
    path('shelfUser/<int:pk>/', user_details, name='user-details'),
]
