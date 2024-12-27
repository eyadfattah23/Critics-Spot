from django.urls import path
from . import views
from users.views import user_details

urlpatterns = [
    path('communities/', views.communities_list),
    path('communities/users/<int:pk>', user_details, name='user_details'),
    path('communities/owner/<int:pk>', user_details, name='owner_details'),
    path('communities/<int:id>', views.community_details),
]
