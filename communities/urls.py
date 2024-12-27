from django.urls import path
from . import views

urlpatterns = [
    path('communities/', views.communities_list, name='communities-list'),
    path(
        'communities/<int:pk>',
        views.community_details,
        name='community-details'
    ),
    path(
        'communities/<int:pk>/posts', views.community_posts,
        name='community-posts'
    ),
    path(
        'communities/<community_id>/posts/<post_id>/comments',
        views.community_posts_comments,
        name='post-comments'
    ),
]
