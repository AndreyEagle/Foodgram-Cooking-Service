from django.contrib import admin
from users.models import User, Subscriptions
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    search_fields = (
        'user__username',
        'user__email',
        'author__username',
        'author__email'
    )
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
