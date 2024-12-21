from django.urls import path, include
import debug_toolbar
from . import views


urlpatterns = [
    path('hello/', views.say_hello),  # always end routes with /
    path('hellot/', views.say_hello_template),  # always end routes with /
    path('__debug__/', include(debug_toolbar.urls))
]
