# -*- encoding: utf-8 -*-
from django.urls import path, include
from api import views, views_domru2, views_beeline, views_mts
from api import views_beeline2, views_rostelecom2, views_rostelecom
from api import views_domru, views_ttk, views_onlime, views_mgts, views_txv
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="Схема API Fullstats",
        default_version='v1',
        description='''Возможности API позволяют зарегистрироваться в сервисе,
            читать ленту новостей, отслеживать понравившиеся и избранные
            новости, иметь возможность оценивать рейтинг новости и количество
            просмотров, а также написать собственную статью.
        ''',
        terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="jason@jaseci.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


app_name = 'api'

router = DefaultRouter()
router.register('set_pv_result', views.SetPvResultViewSet, basename='setpvresult')

urlpatterns = [
    path('get_liza_phrases/<int:num_group>', views.get_liza_phrases, name='liza_phrases'),
    path('get_liza_files/<str:filename>', views.get_liza_files),
    path('get_name_files/<str:filename>', views.get_name_files),
    path('get_names', views.get_names, name='names'),

    path('get_ndz_phrases/<int:num_group>', views.get_ndz_phrases, name='ndz_phrases'),
    path('get_pz_phrases/<int:num_group>', views.get_pz_phrases, name='pz_phrases'),

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

    path('set_bid_onlime', views_onlime.set_bid_onlime),
    path('get_bid_onlime', views_onlime.get_bid_onlime),
    path('set_bid_onlime_status', views_onlime.set_bid_onlime_status),

    path('set_bid_mgts', views_mgts.set_bid_mgts),
    path('get_bid_mgts', views_mgts.get_bid_mgts),
    path('set_bid_mgts_status', views_mgts.set_bid_mgts_status),

    path('set_txv', views_txv.set_txv),
    path('get_txv', views_txv.get_txv),
    path('set_txv_status', views_txv.set_txv_status),

    path('get_bots_info/<str:from_date>', views.get_bots_info),
    path('get_bots_vizit', views.get_bots_vizit),
    path('get_lk_access', views.get_lk_access),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),

    path('get_pv_result/<int:pv_code>/<str:from_date>', views.get_pv_result),
    path('', include(router.urls)),
]
