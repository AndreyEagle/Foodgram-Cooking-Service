# Generated by Django 2.2.16 on 2022-04-06 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Рецепт в избранном',
                'verbose_name_plural': 'Избранные рецепты',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите название ингредиента', max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(help_text='Задайте единицу измерения', max_length=20, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': ('Ингредиент',),
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientsRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='Укажите количество ингредиента', verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Укажите название рецепта', max_length=20, verbose_name='Название')),
                ('image', models.ImageField(help_text='Загрузите изображение рецепта', upload_to='recipes/images/', verbose_name='Изображение')),
                ('text', models.CharField(help_text='Задайте описание рецепта', max_length=255, verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Укажите время приготовления', verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Задайте имя тэга', max_length=200, unique=True, verbose_name='Имя')),
                ('color', models.CharField(help_text='Задайте цвет', max_length=7, unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Задайте уникальный слаг', max_length=200, unique=True, verbose_name='Cлаг')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Tэги',
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Укажите рецепт', on_delete=django.db.models.deletion.CASCADE, to='foodgram.Recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(help_text='Укажите тэг', on_delete=django.db.models.deletion.CASCADE, to='foodgram.Tag', verbose_name='Тэг')),
            ],
            options={
                'verbose_name': 'Тег рецепта',
                'verbose_name_plural': 'Теги рецепта',
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_list', to='foodgram.Recipe', verbose_name='Рецепты')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
    ]
