from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, SubscribeViewSet, SubscriptionsView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'users/(?P<user_id>\d+)/subscribe',
    SubscribeViewSet,
    basename='subscribe'
)

urlpatterns = [
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),

]
