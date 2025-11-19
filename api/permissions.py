from rest_framework import permissions

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "profile", None) and request.user.profile.role == "client")

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "profile", None) and request.user.profile.role == "employee")

class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "profile", None) and request.user.profile.role == "admin")
