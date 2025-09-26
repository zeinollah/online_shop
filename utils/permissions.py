from rest_framework import permissions

class IsProfileOwnerOrSuperuser(permissions.BasePermission):
    """
    This class check the user before update action on Customer Profile to make sure
    the owner or admin try to update and edit profile.
    """

    message = 'You DO NOT have permission to do this.'

    def has_object_permission(self, request, view, obj):
        return obj.account == request.user or (request.user.is_superuser or request.user.is_staff)
