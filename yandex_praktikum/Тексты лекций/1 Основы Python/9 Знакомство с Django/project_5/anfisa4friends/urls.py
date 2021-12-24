from django.urls import path
from homepage import views as home_views

urlpatterns = [
    path('', home_views.index),
]
