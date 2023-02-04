from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.is_admin


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.is_moderator
