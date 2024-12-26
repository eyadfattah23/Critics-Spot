from django.urls import path
from . import views

urlpatterns = [
    path('communities/', views.communities_list),
    path('communities/<int:id>', views.community_details),
]
