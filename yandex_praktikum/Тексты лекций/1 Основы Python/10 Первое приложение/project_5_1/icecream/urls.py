from django.urls import path
from . import views

urlpatterns = [
    path('', views.icecream_list),
    path('<int:pk>/', views.icecream_detail),
    # Добавьте сюда path() с переменной pk типа int и вызовом icecream_detail()
]
