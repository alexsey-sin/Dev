# -*- encoding: utf-8 -*-
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'app'

urlpatterns = [
    path('', views.index, name='home'),
    path('names', views.names, name='names'),

    path('lizagroup', views.lizagroup, name='lizagroup'),
    path('lizaphrases/<str:id_group>', views.lizaphrases, name='lizaphrases'),

    path('germangroup', views.germangroup, name='germangroup'),
    path('germanphrases/<str:id_group>', views.germanphrases, name='germanphrases'),
    path('germananswers/<str:id_group>', views.germananswers, name='germananswers'),

    path('backup', views.backup, name='backup'),
    path('restore', views.restore, name='restore'),

    path('load', views.load, name='load'),
    path('clear', views.clear, name='clear'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)