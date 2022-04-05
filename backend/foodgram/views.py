from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import User

from foodgram.filters import IngredientFilter, RecipeFilter
from foodgram.models import (Favorite, Ingredient, IngredientsRecipe, Recipe,
                             ShoppingList, Tag)
from foodgram.pagination import RecipeLimitPagination
from foodgram.permissions import CheckingUserIsAuthor
from foodgram.serializers import (FavoriteSerializer, IngredientSerializer,
                                  RecipeGetSerializer, RecipeSerializer,
                                  ShoppingCartSerializer, TagSerializer)
from django.conf import settings

DELETE_RECIPE_ERROR = 'Рецепта нет в избранном'
DELETE_SHOPLIST_ERROR = 'Рецепта нет в покупках'
CONTENT_TYPE = 'text/plain'


class CreateDestroyModelViewSet(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    pass


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name', 'name')
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = RecipeLimitPagination
    permission_classes = (CheckingUserIsAuthor, IsAuthenticatedOrReadOnly)
    lookup_field = 'id'
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeSerializer

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientsRecipe.objects.filter(
            recipe__shopping_list_recipe__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(total=Sum('amount'))
        shopping_list = 'список покупок:\n'
        for number, ingredient in enumerate(ingredients, start=1):
            shopping_list += (
                f'{number} '
                f'{ingredient["ingredient__name"]}'
                f'({ingredient["ingredient__measurement_unit"]}) - '
                f'{ingredient["total"]} \n'
            )
        shopping = settings.SHOPPING
        response = HttpResponse(shopping_list, content_type=CONTENT_TYPE)
        response['Content-Disposition'] = (f'attachment;'
                                           f'filename={shopping}')
        return response


class FavoriteViewSet(CreateDestroyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        serializer.save(user=user, recipe=recipe)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        favorite = Favorite.objects.filter(
            user=self.request.user,
            recipe=recipe
        )
        if not favorite.exists():
            raise exceptions.ValidationError(DELETE_RECIPE_ERROR)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(CreateDestroyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        serializer.save(user=user, recipe=recipe)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        shopping_list = ShoppingList.objects.filter(
            user=self.request.user,
            recipe=recipe
        )
        if not shopping_list.exists():
            raise exceptions.ValidationError(DELETE_SHOPLIST_ERROR)
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
