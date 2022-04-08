from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (SubscribeViewSet, SubscriptionsView,
                         TokenCreateView, TokenDestroyView, UserViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'users/(?P<user_id>\d+)/subscribe',
    SubscribeViewSet,
    basename='subscribe'
)

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionsView.as_view(),
        name='subscriptions'
    ),
    path('', include(router.urls)),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]
