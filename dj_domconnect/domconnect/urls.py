# -*- encoding: utf-8 -*-
from django.urls import path
from domconnect import views


app_name = 'domconnect'

urlpatterns = [
    path('', views.index, name='home'),
    path('datacrm', views.dataCrm, name='datacrm'),
    path('dataajax', views.dataAjax, name='dataajax'),

    path('del_all', views.deleteAllLids),
]
