from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOnly(BasePermission):
    """Доступно только для Админа"""
    def has_permission(self, request, view):
        return request.user.is_admin


class AdminOrReadOnlyPermission(permissions.BasePermission):
    """Для categories, genres и titles"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class ReviewCommentsPermission(permissions.BasePermission):
    """Для reviews и comments"""
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.is_admin
                         or request.user.is_moderator)))
