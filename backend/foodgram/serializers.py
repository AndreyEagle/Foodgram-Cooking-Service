from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from users.models import User
from users.serializers import RecipeUserSerializer, UserSerializer

from foodgram.models import (Favorite, Ingredient, IngredientsRecipe, Recipe,
                             ShoppingList, Tag)
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

TAG_VALIDATION_ERROR = 'Теги обязательны для заполнения'
INGREDIENT_VALIDATE_ERROR = 'Добавьте ингредиенты'
INGREDIENT_UNIQUE_ERROR = 'Ингредиенты должны быть разными'
AMOUNT_VALIDATE_ERROR = 'Количество ингредиента должно быть больше 0!'
COOKING_TIME_ERROR = 'Время приготовления должно быть больше 0'
RECIPE_ADD_UNVALIDATED = 'Рецепт уже добавлен в избранное'
SHOPLIST_ADD_UNVALIDATED = 'Рецепт уже добавлен в покупки'


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=(UniqueValidator(queryset=Tag.objects.all()),)
    )
    color = serializers.CharField(
        validators=(UniqueValidator(queryset=Tag.objects.all()),)
    )
    slug = serializers.SlugField(
        validators=(UniqueValidator(queryset=Tag.objects.all()),)
    )

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source='ingredient.id')
    name = serializers.CharField(read_only=True, source='ingredient.name')
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientsRecipePostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'amount')
        constraints = (
            UniqueTogetherValidator(
                queryset=IngredientsRecipe.objects.all(),
                fields=('recipe', 'ingredient'),
            ),
        )


class RecipeGetSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients',
        read_only=True
    )
    image = Base64ImageField(read_only=True)
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited',
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'name',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        queryset = IngredientsRecipe.objects.filter(recipe=obj)
        return RecipeIngredientGetSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingList.objects.filter(
            user=user,
            recipe=obj
        ).exists()


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientsRecipePostSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, data):
        ingredients = self.initial_data['ingredients']
        if not ingredients:
            raise serializers.ValidationError(INGREDIENT_VALIDATE_ERROR)
        return data

    def validate_tags(self, data):
        tags = self.initial_data['tags']
        if not tags:
            raise serializers.ValidationError(TAG_VALIDATION_ERROR)
        return data

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(COOKING_TIME_ERROR)
        return value

    def add_to_ingredients(self, ingredients, recipe):
        ingredients_check = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            name_ingredient = ingredient['id']
            if name_ingredient in ingredients_check:
                raise serializers.ValidationError(INGREDIENT_UNIQUE_ERROR)
            ingredients_check.append(name_ingredient)
            if int(amount) <= 0:
                raise serializers.ValidationError(
                    f'{name_ingredient.name} : {AMOUNT_VALIDATE_ERROR}'
                )
            IngredientsRecipe.objects.create(
                ingredient=name_ingredient,
                recipe=recipe,
                amount=amount
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        self.add_to_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data['tags']
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.add_to_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerializer(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )
        constraints = (
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
            ),
        )

    def validate(self, data):
        user = get_object_or_404(
            User,
            username=self.context['request'].user
        )
        recipe = get_object_or_404(
            Recipe,
            id=self.context['view'].kwargs.get('id')
        )
        is_already_add = Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).exists()
        if is_already_add:
            raise serializers.ValidationError(RECIPE_ADD_UNVALIDATED)
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        instance = get_object_or_404(
            Recipe,
            id=self.context['view'].kwargs.get('id')
        )
        return RecipeUserSerializer(instance, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ShoppingList
        fields = (
            'user',
            'recipe'
        )
        constraints = (
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
            ),
        )

    def validate(self, data):
        user = get_object_or_404(
            User,
            username=self.context['request'].user
        )
        recipe = get_object_or_404(
            Recipe,
            id=self.context['view'].kwargs.get('id')
        )
        already_add = ShoppingList.objects.filter(
            user=user,
            recipe=recipe
        ).exists()
        if already_add:
            raise serializers.ValidationError(SHOPLIST_ADD_UNVALIDATED)
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        instance = get_object_or_404(
            Recipe,
            id=self.context['view'].kwargs.get('id')
        )
        return RecipeUserSerializer(instance, context=context).data
