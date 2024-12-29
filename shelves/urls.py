from django.urls import path
from . import views

urlpatterns = [
    path('shelves/', views.shelves_list),
    path('shelves/user/<int:user_id>/', views.users_shelves),
]
