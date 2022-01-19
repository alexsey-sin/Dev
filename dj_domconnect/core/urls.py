# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', include('demo.urls')),
    path('api/', include('api.urls')),
    path('mobile/', include('mobile.urls')),
    path('domconnect/', include('domconnect.urls')),
    path('', include('app.urls')),
    path('', include('authentication.urls')),
    path('api-token-auth/', views.obtain_auth_token),
]
