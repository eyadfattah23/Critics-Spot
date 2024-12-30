from django.urls import path
from . import views


urlpatterns = [
    path('communities/', views.CommunityList.as_view(), name='communities-list'),
    path(
        'communities/<int:pk>/',
        views.CommunityDetail.as_view(),
        name='community-details'
    ),
    path(
        'communities/<int:pk>/posts/', views.CommunityPost.as_view(),
        name='community-posts'
    ),
    path(
        'posts/<int:pk>/comments/',
        views.CommunityPostComments.as_view(),
        name='community-post-comments'
    ),
    path(
        'posts/<int:pk>/likes/',
        views.CommunityPostLikes.as_view(),
        name='community-post-likes'
    ),
    path(
        'posts/<int:pk>/',
        views.CommunityPostDetail.as_view(),
        name='community-post-details'
    ),
    path(
        'comments/<int:pk>/',
        views.CommunityPostCommentDetail.as_view(),
        name='community-post-comment-details'
    ),

    path(
        'likes/<int:pk>/',
        views.CommunityPostLikeDetail.as_view(),
        name='community-post-like-details'
    ),
    path(
        'communities/<int:pk>/members/join/',
        views.CommunityMemberList.as_view(),
        name='add-member'
    ),

    path(
        'communities/<int:pk>/members/leave/',
        views.CommunityMemberList.as_view(),
        name='remove-member'
    )
]
