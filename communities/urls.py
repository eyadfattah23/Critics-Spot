from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('communities', views.CommunityViewSet)
router.register('posts', views.CommunityPostViewSet)
router.register('comments', views.CommunityPostCommentsViewSet)

urlpatterns = [ 
    router.urls,
    path('communities/<int:pk>/members/', views.CommunityMemberList.as_view(), name='community-members'),
    path('posts/<int:pk>/likes/', views.CommunityPostLikes.as_view(), name='community-post-likes')
]
