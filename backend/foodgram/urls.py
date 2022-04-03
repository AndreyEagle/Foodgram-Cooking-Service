from django.urls import include, path
from rest_framework.routers import DefaultRouter

from foodgram.views import (FavoriteViewSet, IngredientsViewSet, RecipeViewSet,
                            TagViewSet, ShoppingCartViewSet)

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(
    r'recipes/(?P<id>\d+)/favorite',
    FavoriteViewSet,
    basename='favorite'
)
router.register(
    r'recipes/(?P<id>\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart'
)

urlpatterns = [
    path('', include(router.urls)),
]
