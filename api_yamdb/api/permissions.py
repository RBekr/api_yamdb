from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_moderator
