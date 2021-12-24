# posts/urls.py
from django.urls import path, include
from .views import PostList, PostDetail
from django.contrib import admin
from rest_framework.authtoken import views


urlpatterns = [
    path('api/v1/posts/', PostList.as_view()),
    path('api/v1/posts/<int:pk>/', PostDetail.as_view()),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
