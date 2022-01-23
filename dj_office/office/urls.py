# -*- encoding: utf-8 -*-
from django.urls import path
from office import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'office'

urlpatterns = [
    path('', views.index, name='home'),
    path('moexbond', views.moexbond, name='moexbond'),
    path('dwnldmoexbond', views.download_moex, name='dwnldmoexbond'),

    path('testbond', views.testbond, name='testbond'),
    # path('lizaphrases/<str:id_group>', views.lizaphrases, name='lizaphrases'),

    # path('germangroup', views.germangroup, name='germangroup'),
    # path('germanphrases/<str:id_group>', views.germanphrases, name='germanphrases'),
    # path('germananswers/<str:id_group>', views.germananswers, name='germananswers'),

    # path('ndzgroup', views.ndzgroup, name='ndzgroup'),
    # path('ndzphrases/<str:id_group>', views.ndzphrases, name='ndzphrases'),

    # path('pzgroup', views.pzgroup, name='pzgroup'),
    # path('pzphrases/<str:id_group>', views.pzphrases, name='pzphrases'),

    # path('backup', views.backup, name='backup'),
    # path('restore', views.restore, name='restore'),

    # path('load', views.load, name='load'),
    # path('clear', views.clear, name='clear'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)