from rest_framework.permissions import BasePermission
from rest_framework import permissions


class CheckingUserIsAuthor(BasePermission):
    message = 'Изменение или удаление чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
