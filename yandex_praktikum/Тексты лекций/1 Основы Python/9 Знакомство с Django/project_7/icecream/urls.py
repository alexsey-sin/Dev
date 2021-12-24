from django.urls import path
from . import views

urlpatterns = [
    path('', views.icecream_list),
    # здесь должен быть path(), который
    # при обращении к странице /icecream/
    # вызовет функцию icecream_list() из views.py
    # # [примечание] при include запрошенный URL в присоединяемом файле
    # указывается не полностью
]
