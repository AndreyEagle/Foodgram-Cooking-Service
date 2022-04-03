from django.contrib import admin
from foodgram.models import Ingredient, Recipe, Tag, Favorite, ShoppingList


class TagInline(admin.TabularInline):
    model = Recipe.tags.through


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',

    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'image',
        'text',
        'cooking_time'
    )
    search_fields = ('name', 'author')
    empty_value_display = '-пусто-'
    inlines = [
        TagInline,
        IngredientsInline
    ]


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',

    )
    empty_value_display = '-пусто-'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
