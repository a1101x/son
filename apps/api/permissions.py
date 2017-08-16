from rest_framework.permissions import BasePermission
from rest_framework.compat import is_authenticated
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or
            request.user and is_authenticated(request.user) and request.user.is_admin
        )
