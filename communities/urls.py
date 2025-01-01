from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
from . import views

router = DefaultRouter()

router.register('users', CustomUserViewSet, basename='customuser')
router.register('communities', views.CommunityViewSet, basename='community')
router.register('posts', views.CommunityPostViewSet, basename='communitypost')
router.register('comments', views.CommunityPostCommentsViewSet, basename='communitypostcomment')
router.register('likes', views.CommunityPostLikesViewSet, basename='communitypostlike')

urlpatterns = [
    path('', include(router.urls)),
    path('communities/<int:pk>/members/join/', views.CommunityMemberList.as_view(), name='community-members'),
    path('communities/<int:pk>/members/leave/', views.CommunityMemberList.as_view(), name='community-members'),
]
