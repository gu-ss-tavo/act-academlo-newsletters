from rest_framework import permissions

from user.models import CustomUser

class IsActionForUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(request.user, CustomUser):
            return True
        return False

class IsSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False
