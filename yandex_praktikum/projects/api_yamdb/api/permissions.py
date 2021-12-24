from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrDjangoAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in (
                'POST', 'DELETE', 'PATCH') and request.user.is_authenticated:
            return request.user.is_admin
        return request.method == 'GET'


class IsModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_moderator or obj.author == request.user:
                return True
        return request.method in permissions.SAFE_METHODS
