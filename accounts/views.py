from django.utils import timezone
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EmailVerificationToken
from .serializers import (
    RegistrationSerializer,
    UpdateUserSerializer,
    LoginSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    ResendVerificationSerializer,
)
from .permissions import CurrentUserOrAdmin
from utils.emails import send_verification_email




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
        user = serializer.save()
        token = EmailVerificationToken.objects.create(user=user)

        try:
            send_verification_email(user, token)
        except Exception:
            token.delete()
            return Response(
                {"message": "Registration successful but we could not send the verification email."
                            " Please use the resend verification option."},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {"message": "Registration successful. Please check your email to verify your account."},
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

"""Change Password"""

class ChangePasswordViewSet(viewsets.GenericViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password changed"},
            status=status.HTTP_200_OK
        )




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


"""Email Verification Views"""
class VerifyEmailViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    http_method_names = ['get']

    def retrieve(self, request, pk=None, *args, **kwargs):

        try:
            token = EmailVerificationToken.objects.get(token=pk)
        except EmailVerificationToken.DoesNotExist:
            return Response(
                {"message": "Invalid verification link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not token.is_valid():
            token.delete()
            return Response(
                {"message": "This verification link has expired. Please request a new one."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token.user
        profile = self._get_profile(user)


        if not profile:
            return Response(
                {"message": "User profile does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if profile.is_verified:
            return Response(
                {"message": "User account is already verified"},
                status=status.HTTP_400_BAD_REQUEST
            )

        profile.is_verified = True
        profile.save()

        token.is_used = True
        token.save()

        return Response(
            {"message": "Email verified successfully. You can now log in."},
            status=status.HTTP_200_OK
        )

    def _get_profile(self, user):
        if hasattr(user, 'customer_profile'):
            return user.customer_profile
        if hasattr(user, 'seller_profile'):
            return user.seller_profile
        return None


class ResendVerificationViewSet(viewsets.GenericViewSet):
    serializer_class = ResendVerificationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.context['user']

        EmailVerificationToken.objects.filter(user=user).delete()
        token = EmailVerificationToken.objects.create(user=user)

        try:
            send_verification_email(user, token, subject="Resend verification email")

        except Exception:
            token.delete()
            return Response(
                {"message": "Failed to send verification email. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"message": "Verification email sent. Please check your inbox."},
            status=status.HTTP_200_OK
        )