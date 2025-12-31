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

        if hasattr(obj, 'customer'):# for order
            if hasattr(user, 'customer_profile'):
                return obj.customer == user.customer_profile

        if hasattr(obj, 'order'): # for order item
            if hasattr(user, 'customer_profile'):
                return obj.order.customer == user.customer_profile

        return False



class IsDiscountOwnerOrSuperuser(permissions.BasePermission):
    """
    Make sure each seller can access to their discount code not another.
    """

    message = 'You DO NOT access to this discount.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True

        if hasattr(obj, 'seller'):
            if hasattr(user, 'seller_profile'):
                return obj.seller == user.seller_profile

        return True