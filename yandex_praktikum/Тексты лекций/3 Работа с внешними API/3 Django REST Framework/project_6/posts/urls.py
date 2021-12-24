from django.urls import path
from rest_framework.authtoken import views
from .views import APIPost, APIPostDetail

urlpatterns = [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/posts/', APIPost.as_view()),
    path('api/v1/posts/<int:id>/', APIPostDetail.as_view()),
]
