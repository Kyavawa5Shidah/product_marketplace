from rest_framework.permissions import BasePermission


class IsBusinessAdmin(BasePermission):
    """
    Allows access only to users with ADMIN role.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role and
            request.user.role.name == 'ADMIN'
        )
