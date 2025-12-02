from rest_framework import permissions


class IsSellerProfileOwnerOrSuperuser(permissions.BasePermission):
    """
    This class check the user before all actions to make sure user is admin or owner for seller.
    """

    message = 'You DO NOT have permission to do this action.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        return obj.account == user


class IsCustomerProfileOwnerOrSuperuser(permissions.BasePermission):
    """
    This class check the user before all actions to make sure user is admin or owner for customer.
    """
    message = 'You DO NOT have permission to do this action.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        return obj.account == user


class IsOrderOwnerOrSuperuser(permissions.BasePermission):
    """
    This class check only customer or admin can cancel the order.
    """

    message = 'You can NOT DO this action.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True

        if hasattr(user, 'customer_profile'):
            return obj.account == user.customer_profile

        return False