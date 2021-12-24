# -*- encoding: utf-8 -*-
from django.urls import path
from mobile import views
# from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )


app_name = 'mobile'

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),
    # path('api-auth', include('rest_framework.urls')),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api', views.api, name='api'),
    path('', views.index, name='home'),

    path('numsetting', views.numsetting, name='numsetting'),
    path('numcondition', views.numcondition, name='numcondition'),
    path('get_mobile_residue', views.get_mobile_residue, name='get_mobile_residue'),

    # path('germangroup', views.germangroup, name='germangroup'),
    # path('germanphrases/<str:id_group>', views.germanphrases, name='germanphrases'),
    # path('germananswers/<str:id_group>', views.germananswers, name='germananswers'),

    # path('backup', views.backup, name='backup'),
    # path('restore', views.restore, name='restore'),

    # path('load', views.load, name='load'),
    # path('clear', views.clear, name='clear'),
]
