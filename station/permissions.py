from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAllOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and request.user and request.user.is_authenticated
        ) or (
            request.user.is_staff
        )
