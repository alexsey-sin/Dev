from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (get_confirmation_code, get_jwt_token, UserViewSet,
                    TitleViewSet, CategoryViewSet, GenreViewSet,
                    ReviewViewSet, CommentViewSet)


router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet)
router_v1.register('titles/(?P<title_id>[^/.]+)/reviews', ReviewViewSet,
                   basename='titles')
router_v1.register(
    'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/email/', get_confirmation_code),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/me/', UserViewSet.as_view({'patch': 'partial_update'})),
]
