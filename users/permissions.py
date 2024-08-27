from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
