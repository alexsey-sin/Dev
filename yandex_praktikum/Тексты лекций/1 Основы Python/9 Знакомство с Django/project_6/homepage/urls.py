from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    # Тут должен быть path(), который при обращении к главной странице
    # вызовет view-функцию index() из файла views.py
]
