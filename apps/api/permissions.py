from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS and not request.user.is_blocked or
            request.user and is_authenticated(request.user) and request.user.is_admin and not request.user.is_blocked
        )


class IsOwnerOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS and not request.user.is_blocked or
            obj.user == request.user and not request.user.is_blocked
        ) 

class IsBlocked(BasePermission):
    
    def has_permission(self, request, view):
        return (
            request.user and is_authenticated(request.user) and not request.user.is_blocked
        )
