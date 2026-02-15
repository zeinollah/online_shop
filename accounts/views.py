from django.utils import timezone
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import (
    RegistrationSerializer,
    UpdateUserSerializer,
    LoginSerializer,
    LogoutSerializer,
    )
from .permissions import CurrentUserOrAdmin




User = get_user_model()

"""CRUD Views"""

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

"""Login / Logout Views"""

class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response(
            {"message": "Login successful",
             "access_token": str(access_token),
             "refresh_token": str(refresh),
             "user": {
                 "email": user.email,
                 "first_name": user.first_name,
                 "last_name": user.last_name,
                 "role": user.user_role,
             }},
            status=status.HTTP_200_OK
        )


class LogoutViewSet(viewsets.GenericViewSet):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_200_OK
            )

        except KeyError as e:
            return Response(
                {"error": f"Token validation failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
