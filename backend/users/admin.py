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
    search_fields = ('username',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    search_fields = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
