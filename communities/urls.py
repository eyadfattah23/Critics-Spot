from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'communities', views.CommunityViewSet, basename='community')

communities_router = routers.NestedDefaultRouter(
    router, r'communities', lookup='community')
communities_router.register(
    r'posts', views.CommunityPostViewSet, basename='community-posts')

posts_router = routers.NestedDefaultRouter(
    communities_router, r'posts', lookup='post')
posts_router.register(r'comments', views.PostCommentViewSet,
                      basename='post-comments')

urlpatterns = [
    *router.urls,
    *communities_router.urls,
    *posts_router.urls,
]
