from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from foodgram.models import Recipe
from rest_framework import serializers

from users.models import Subscriptions, User

INVALID_EMAIL_OR_PASSWORD = 'Неверные электронная почта или пароль'
SUBS_VALIDATE_ERROR = 'Нельзя подписаться на самого себя!'
ALREADY_FOLLOW = 'Вы уже подписаны!'
INVALID_PASSWORD = 'Неверный пароль'


class UserPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )


class UserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        if request.user.is_anonymous:
            return False
        return Subscriptions.objects.filter(
            user=request.user,
            author=obj
        ).exists()


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=254,
    )
    password = serializers.CharField(
        max_length=150,
    )

    def validate(self, data):
        user_check = User.objects.filter(email=data['email']).exists()
        if user_check:
            user = User.objects.get(email=data['email'])
            password_valid = user.check_password(data['password'])
            if password_valid:
                return data
        raise serializers.ValidationError(INVALID_EMAIL_OR_PASSWORD)


class UserChangePassSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    current_password = serializers.CharField()

    def validate_new_password(self, value):
        validate_password(value, self.context['request'].user)
        return value

    def validate_current_password(self, value):
        is_password_valid = self.context['request'].user.check_password(value)
        if is_password_valid:
            return value
        raise serializers.ValidationError(INVALID_PASSWORD)


class RecipeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubsSerializer(UserGetSerializer):
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes',
        read_only=True
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count',
        read_only=True
    )

    class Meta(UserGetSerializer.Meta):
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        context = {'request': request}
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = obj.recipes.all()
            recipes = recipes[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        return RecipeUserSerializer(recipes, many=True, context=context).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscriptions
        fields = ('user', 'author')

    def validate(self, data):
        user = get_object_or_404(
            User, username=self.context['request'].user
        )
        author = get_object_or_404(
            User,
            id=self.context['view'].kwargs.get('user_id')
        )
        if user == author:
            raise serializers.ValidationError(SUBS_VALIDATE_ERROR)
        already_subs = Subscriptions.objects.filter(
            user=user,
            author=author
        ).exists()
        if already_subs:
            raise serializers.ValidationError(ALREADY_FOLLOW)
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        instance = get_object_or_404(
            User,
            id=self.context['view'].kwargs.get('user_id')
        )
        return SubsSerializer(instance, context=context).data
