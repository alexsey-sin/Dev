# -*- encoding: utf-8 -*-
from django.urls import path
from domconnect import views


app_name = 'domconnect'

urlpatterns = [
    path('', views.index, name='home'),
    path('datacrm', views.dataCrm, name='datacrm'),
    path('dataajax', views.dataAjax, name='dataajax'),

    path('del_all_lids', views.deleteAllLids),
    path('del_cash', views.deleteCash),
    path('del_all_deals', views.deleteAllDeals),
    path('upgrade_site_source', views.upgradeSiteSource),
]
