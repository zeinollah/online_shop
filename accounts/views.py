from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import (RegistrationSerializer,
                          UpdateUserSerializer,
                          )
from .permissions import CurrentUserOrAdmin




User = get_user_model()

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User registered",},
             status=status.HTTP_201_CREATED
        )


class UserInfoViewSet(viewsets.ReadOnlyModelViewSet):


    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [CurrentUserOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)


class UpdateUserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [CurrentUserOrAdmin]

    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
             {"message": "User account updated",},
                   status=status.HTTP_200_OK
        )


class DeleteUserViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [CurrentUserOrAdmin]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "User account deleted"},
            status=status.HTTP_200_OK
        )


# TODO = Replace the local permission class by utils permission class