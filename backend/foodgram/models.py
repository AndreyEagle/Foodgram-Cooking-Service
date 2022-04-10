
from django.db import models
from users.models import User
from django.core.validators import MinValueValidator

COOKING_TIME_ERROR = 'Время приготовления должно быть больше 0'
AMOUNT_VALIDATE_ERROR = 'Количество ингредиента должно быть больше 0!'


class Tag(models.Model):
    name = models.CharField(
        'Имя',
        unique=True,
        max_length=200,
        help_text='Задайте имя тэга'
    )
    color = models.CharField(
        'Цвет',
        unique=True,
        max_length=7,
        help_text='Задайте цвет'
    )
    slug = models.SlugField(
        'Cлаг',
        unique=True,
        max_length=200,
        help_text='Задайте уникальный слаг'
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
        verbose_name='Автор',
        help_text='Укажите автора рецепта'
    )
    name = models.CharField(
        'Название',
        max_length=20,
        help_text='Укажите название рецепта'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
        help_text='Загрузите изображение рецепта'
    )
    text = models.CharField(
        'Описание',
        max_length=255,
        help_text='Задайте описание рецепта'
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
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Укажите время приготовления',
        validators=(MinValueValidator(1, COOKING_TIME_ERROR),),
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Укажите название ингредиента'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=20,
        help_text='Задайте единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тэг',
        help_text='Укажите тэг'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите рецепт'
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_tag'
            ),
        )

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
        verbose_name='Ингредиент',
        help_text='Укажите ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
        verbose_name='Рецепт',
        help_text='Укажите рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        help_text='Укажите количество ингредиента',
        validators=(MinValueValidator(1, AMOUNT_VALIDATE_ERROR),),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
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
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='Пользователь с избранными рецептами'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
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
        help_text='Добавьте пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Рецепты',
        help_text='Добавьте рецепт'
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
