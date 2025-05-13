from rest_framework import permissions

class CurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        # print(f"user is staff: {user.is_staff}, obj pk: {obj.pk}, user pk: {user.pk}")
        return user.is_staff or obj.pk == user.pk