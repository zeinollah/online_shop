from rest_framework import permissions

class IsProfileOwnerOrSuperuser(permissions.BasePermission):
    """
    This class check the user before all actions to make sure user is admin or owner.
    """

    message = 'You DO NOT have permission to do this.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        return obj.seller.account == user
