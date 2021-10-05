from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return False


class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_superuser:
            return True
        return False


class IsAdminOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and (request.user.is_staff or request.user.is_superuser):
            return True
        return False


class IsCustomer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_customer:
            return True
        return False
