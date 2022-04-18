# -*- encoding: utf-8 -*-
from django.urls import path
from domconnect import views


app_name = 'domconnect'

urlpatterns = [
    path('', views.index, name='home'),
    path('sites', views.sites, name='sites'),
    path('site_edit/<int:id_site>', views.site_edit, name='site_edit'),
    path('sources', views.sources, name='sources'),
    path('datacrm', views.dataCrm, name='datacrm'),
    path('dataajax', views.dataAjax, name='dataajax'),

    path('del_all_lids', views.deleteAllLids),
    path('del_cash', views.deleteCash),
    path('del_all_deals', views.deleteAllDeals),
    path('upgrade_site_source', views.upgradeSiteSource),

    path('upgrade_seo', views.upgradeSeo),
]
