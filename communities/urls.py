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
        'posts/<int:pk>/comments',
        views.community_post_comments,
        name='community-post-comments'
    ),
    path(
        'posts/<int:pk>/likes',
        views.community_post_likes,
        name='community-post-likes'
    ),
    path(
        'communities/<community_id>/posts/<post_id>',
        views.community_post_details,
        name='community-post-details'
    ),
    path(
        'posts/<int:pk>/comments/<int:comment_id>',
        views.community_post_comment_details,
        name='community-post-comment-details'
    ),

    path(
        'posts/<int:pk>/likes/<int:like_id>',
        views.community_post_like_details,
        name='community-post-like-details'
    )
]
