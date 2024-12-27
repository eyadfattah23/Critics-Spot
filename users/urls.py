from django.urls import path, include
from . import views 
import shelves.views


urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:pk>', views.user_details),
    path('shelves/<int:pk>', shelves.views.shelf_details, name='shelf-details')
]
