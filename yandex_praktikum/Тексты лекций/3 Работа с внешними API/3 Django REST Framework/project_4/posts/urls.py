#  импортируйте в код всё необходимое
from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/posts/<int:post_id>/', views.get_post),
]
