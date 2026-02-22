from rest_framework.routers import DefaultRouter
from .views import (
    RegistrationViewSet,
    UserInfoViewSet,
    UpdateUserViewSet,
    DeleteUserViewSet,
    LoginViewSet,
    LogoutViewSet,
    ChangePasswordViewSet,
    VerifyEmailViewSet,
    ResendVerificationViewSet
)

router = DefaultRouter()

"""CRUD Patch"""
router.register(r'register', RegistrationViewSet, basename='register')
router.register(r'userinfo', UserInfoViewSet, basename='userinfo')
router.register(r'user-update', UpdateUserViewSet, basename='user-update')
router.register(r'user-delete', DeleteUserViewSet, basename='user-delete')


"""Login / Logout Patch"""
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')


"""Change Password"""
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')

"""Email Verification routes"""
router.register(r'verify-email', VerifyEmailViewSet, basename='verify-email')
router.register(r'resend-verification', ResendVerificationViewSet, basename='resend-verification')


urlpatterns = router.urls
