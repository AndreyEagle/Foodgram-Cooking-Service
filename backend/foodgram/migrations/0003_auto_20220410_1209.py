# Generated by Django 2.2.16 on 2022-04-10 08:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0002_auto_20220406_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(help_text='Укажите количество ингредиента', validators=[django.core.validators.MinValueValidator(1, 'Количество ингредиента должно быть больше 0!')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Укажите время приготовления', validators=[django.core.validators.MinValueValidator(1, 'Время приготовления должно быть больше 0')], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='recipe',
            field=models.ForeignKey(help_text='Добавьте рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='foodgram.Recipe', verbose_name='Рецепты'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(help_text='Добавьте пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
