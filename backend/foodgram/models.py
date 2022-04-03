
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200
    )
    color = models.CharField(
        unique=True,
        max_length=7,
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Tэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/',
    )
    text = models.CharField(
        max_length=255,
        verbose_name='description'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='tags'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientsRecipe',
        related_name='ingredients'
    )
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
    )
    measurement_unit = models.CharField(
        max_length=20,
    )

    class Meta:
        verbose_name = 'Ингридиент',
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Теги рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'), name='unique_tag'
            ),
        )

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes_ingredient'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe'
    )
    amount = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return self.ingredient.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='all_recipes',
        verbose_name='Пользователь',
        help_text='Пользователь с избранными рецептами'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_favorite',
        verbose_name='Рецепт',
        help_text='Рецепт в избранном'

    )

    class Meta:
        verbose_name = 'Рецепт в избранном'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite'
            ),
        )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list_recipe',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_list',
            ),
        )
