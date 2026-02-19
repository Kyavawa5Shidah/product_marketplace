from rest_framework.permissions import BasePermission


class ProductPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        role = request.user.role

        if not role:
            return False

        if request.method == 'POST':
            return role.can_create_product

        if request.method in ['PUT', 'PATCH']:
            return role.can_edit_product

        if request.method == 'DELETE':
            return role.can_delete_product

        return True  # allow safe methods

    def has_object_permission(self, request, view, obj):

        # Prevent cross-business access
        if obj.business != request.user.business:
            return False

        return True
