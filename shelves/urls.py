from django.urls import path
from . import views

urlpatterns = [
    path('shelves/', views.shelves_list),
    path('shelves/<int:id>/', views.shelf_details),
]
