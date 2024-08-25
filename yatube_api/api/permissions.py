"""Модуль содержит классы разрешений для API проекта Yatube."""
from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Проверка аутентификации и авторства поста/комментария."""

    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        """Проверяет, аутентифицирован ли пользователь."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь автором поста/комментария."""
        return obj.author == request.user
