#!/usr/bin/python3
"""
URL patterns for the communities app.
"""
from rest_framework_nested import routers
from . import views

# Create a router and register the community viewset
router = routers.DefaultRouter()
router.register(r'communities', views.CommunityViewSet, basename='community')

# Create a nested router for community posts
communities_router = routers.NestedDefaultRouter(
    router, r'communities', lookup='community')
communities_router.register(
    r'posts', views.CommunityPostViewSet, basename='community-posts')

# Create a nested router for post comments
posts_router = routers.NestedDefaultRouter(
    communities_router, r'posts', lookup='post')
posts_router.register(r'comments', views.PostCommentViewSet,
                      basename='post-comments')

# Combine all the URLs
urlpatterns = [
    *router.urls,
    *communities_router.urls,
    *posts_router.urls,
]
