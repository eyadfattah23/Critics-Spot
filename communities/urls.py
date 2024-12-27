from django.urls import path
from . import views

urlpatterns = [
    path('communities/', views.communities_list),
    path('communities/<int:pk>', views.community_details),
]
