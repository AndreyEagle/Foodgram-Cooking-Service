from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        'Почта',
        unique=True,
        max_length=254,
        help_text='Укажите почту'
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        help_text='Укажите пароль'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        help_text='Укажите имя'
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        help_text='Укажите фамилию'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscriptions(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписывающийся пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Пользователь с подписчиками'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author',),
                name='unique_follow'
            ),
        )

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
