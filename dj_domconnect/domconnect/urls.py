# -*- encoding: utf-8 -*-
from django.urls import path
from domconnect import views
from django.conf import settings


app_name = 'domconnect'

urlpatterns = [
    path('', views.index, name='home'),
    # path('statseo', views.statseo, name='statseo'),

    path('dwnldlids/<str:from_date>', views.downloadLidsFromCRM, name='downloadLidsFromCRM'),
]
