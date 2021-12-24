# -*- encoding: utf-8 -*-
from django.urls import path
from api import views, views_domru2, views_beeline, views_mts
from api import views_beeline2, views_rostelecom2, views_rostelecom
from api import views_domru, views_ttk, views_txv
from api import views_txv_domru, views_txv_rostelecom, views_txv_beeline, views_txv_mts


app_name = 'api'

urlpatterns = [
    path('get_liza_phrases/<int:num_group>', views.get_liza_phrases),
    path('get_liza_files/<str:filename>', views.get_liza_files),
    path('get_name_files/<str:filename>', views.get_name_files),
    path('get_names', views.get_names),

    path('set_bid_domru2', views_domru2.set_bid_domru2),
    path('get_bid_domru2', views_domru2.get_bid_domru2),
    path('set_bid_domru2_status', views_domru2.set_bid_domru2_status),

    path('set_bid_beeline', views_beeline.set_bid_beeline),
    path('get_bid_beeline', views_beeline.get_bid_beeline),
    path('set_bid_beeline_status', views_beeline.set_bid_beeline_status),

    path('set_bid_mts', views_mts.set_bid_mts),
    path('get_bid_mts', views_mts.get_bid_mts),
    path('set_bid_mts_status', views_mts.set_bid_mts_status),

    path('set_bid_beeline2', views_beeline2.set_bid_beeline2),
    path('get_bid_beeline2', views_beeline2.get_bid_beeline2),
    path('set_bid_beeline2_status', views_beeline2.set_bid_beeline2_status),

    path('set_bid_rostelecom2', views_rostelecom2.set_bid_rostelecom2),
    path('get_bid_rostelecom2', views_rostelecom2.get_bid_rostelecom2),
    path('set_bid_rostelecom2_status', views_rostelecom2.set_bid_rostelecom2_status),

    path('set_bid_rostelecom', views_rostelecom.set_bid_rostelecom),
    path('get_bid_rostelecom', views_rostelecom.get_bid_rostelecom),
    path('set_bid_rostelecom_status', views_rostelecom.set_bid_rostelecom_status),

    path('set_bid_domru', views_domru.set_bid_domru),
    path('get_bid_domru', views_domru.get_bid_domru),
    path('set_bid_domru_status', views_domru.set_bid_domru_status),

    path('set_bid_ttk', views_ttk.set_bid_ttk),
    path('get_bid_ttk', views_ttk.get_bid_ttk),
    path('set_bid_ttk_status', views_ttk.set_bid_ttk_status),

    path('set_txv_beeline', views_txv_beeline.set_txv_beeline),
    path('get_txv_beeline', views_txv_beeline.get_txv_beeline),
    path('set_txv_beeline_status', views_txv_beeline.set_txv_beeline_status),

    path('set_txv_mts', views_txv_mts.set_txv_mts),
    path('get_txv_mts', views_txv_mts.get_txv_mts),
    path('set_txv_mts_status', views_txv_mts.set_txv_mts_status),

    path('set_txv_domru', views_txv_domru.set_txv_domru),
    path('get_txv_domru', views_txv_domru.get_txv_domru),
    path('set_txv_domru_status', views_txv_domru.set_txv_domru_status),

    path('set_txv_rostelecom', views_txv_rostelecom.set_txv_rostelecom),
    path('get_txv_rostelecom', views_txv_rostelecom.get_txv_rostelecom),
    path('set_txv_rostelecom_status', views_txv_rostelecom.set_txv_rostelecom_status),

    path('set_txv', views_txv.set_txv),
    path('get_txv', views_txv.get_txv),
    path('set_txv_status', views_txv.set_txv_status),
]
