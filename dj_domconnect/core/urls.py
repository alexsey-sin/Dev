# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include


auth_patterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('admin/', admin.site.urls),
    path('demo/', include('demo.urls')),
    path('api/', include('api.urls')),
    path('mobile/', include('mobile.urls')),
    path('domconnect/', include('domconnect.urls')),
    path('', include('app.urls')),
    path('', include('authentication.urls')),
]
