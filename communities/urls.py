from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
from . import views

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='customuser')
router.register('communities', views.CommunityViewSet, basename='community')
router.register('posts', views.PostViewSet, basename='post')
router.register('comments', views.CommentViewSet, basename='comment')
router.register('likes', views.LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
]
