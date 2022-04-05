from backend.core import HTTPMethod
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (exceptions, filters, generics, mixins, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import Subscriptions, User
from users.pagination import UserLimitPagination
from users.permissions import CurrentUserOrAdmin
from users.serializers import (SubscribeSerializer, SubsSerializer,
                               UserChangePassSerializer, UserGetSerializer,
                               UserPostSerializer)

UNFOLLOW_ERROR = 'Пользователя нет в подписках'


class CreateDestroyModelViewSet(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    pagination_class = UserLimitPagination
    queryset = User.objects.all()
    lookup_field = 'id'
    filter_backends = (
        DjangoFilterBackend,
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return UserPostSerializer
        if self.action == 'set_password':
            return UserChangePassSerializer
        return UserGetSerializer

    def perform_create(self, serializer):
        password = make_password(serializer.initial_data['password'])
        serializer.save(password=password)

    def get_instance(self):
        return self.request.user

    @action(
        methods=(HTTPMethod.GET,),
        detail=False,
        permission_classes=(CurrentUserOrAdmin, IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(
        methods=(HTTPMethod.POST,),
        detail=False,
        permission_classes=(CurrentUserOrAdmin, IsAuthenticated,),
    )
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.get_instance().set_password(
            serializer.validated_data['new_password']
        )
        self.get_instance().save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsView(generics.ListAPIView):
    queryset = User.objects.all()
    pagination_class = UserLimitPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = SubsSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )

    def get_queryset(self):
        return User.objects.filter(
            following__user=self.request.user
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubscribeViewSet(CreateDestroyModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    pagination_class = UserLimitPagination

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user)
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        serializer.save(user=user, author=author)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        subscribe = Subscriptions.objects.filter(
            user=self.request.user,
            author=author
        )
        if not subscribe.exists():
            raise exceptions.ValidationError(UNFOLLOW_ERROR)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
