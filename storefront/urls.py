#!/usr/bin/python3
"""
URL configuration for storefront project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
import debug_toolbar
from . import settings
from users.views import activate_user, reset_password_confirm
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

admin.site.site_header = 'Critics-Spot Admin'
admin.site.index_title = 'Admin'

# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Critics-Spot API",
        default_version='v1',
        description="API for Critics-Spot project",
        contact=openapi.Contact(email="mohamdhamza123467890@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('books.urls')),
    path('api/', include('shelves.urls')),
    path('api/', include('communities.urls')),
    path('auth/users/activation/<str:uid>/<str:token>/',
         activate_user, name='activate-user'),
    path('auth/users/reset_password_confirm/<str:uid>/<str:token>/',
         reset_password_confirm, name='password-reset-confirm'),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:  # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
