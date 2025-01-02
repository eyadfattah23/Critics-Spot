from django.urls import path
from .views import (
    CommunitiesList, CommunityDetails, CommunityPosts, CommunityPostDetails,
    CommunityPostComments, CommunityPostCommentDetails, CommunityPostLikes,
    CommunityPostLikeDetails, AddMember, RemoveMember
)

urlpatterns = [
    path('communities/', CommunitiesList.as_view(), name='communities_list'),
    path('communities/<int:pk>/', CommunityDetails.as_view(), name='community_details'),
    path('communities/<int:pk>/posts/', CommunityPosts.as_view(), name='community_posts'),
    path('posts/<int:pk>/', CommunityPostDetails.as_view(), name='community_post_details'),
    path('posts/<int:pk>/comments/', CommunityPostComments.as_view(), name='community_post_comments'),
    path('posts/comments/<int:pk>/', CommunityPostCommentDetails.as_view(), name='community_post_comment_details'),
    path('posts/<int:pk>/likes/', CommunityPostLikes.as_view(), name='community_post_likes'),
    path('likes/<int:pk>/', CommunityPostLikeDetails.as_view(), name='community_post_like_details'),
    path('communities/<int:pk>/add_member/', AddMember.as_view(), name='add_member'),
    path('communities/<int:pk>/remove_member/', RemoveMember.as_view(), name='remove_member'),
]
