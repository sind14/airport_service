from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStuffOrReadOnly(BasePermission):
    """
    The request is authenticated as staff, or is a read-only request for anon users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # Дозволяємо перегляд усім, включаючи анонімних користувачів
        return bool(request.user and request.user.is_staff)


class IsAdminOrStuffReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user and request.user.is_staff:
            return True
        return bool(request.user and request.user.is_superuser)