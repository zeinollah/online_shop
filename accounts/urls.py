from rest_framework.routers import DefaultRouter
from .views import (
    RegistrationViewSet,
    UserInfoViewSet,
    UpdateUserViewSet,
    DeleteUserViewSet,
    LoginViewSet,
    LogoutViewSet,
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

urlpatterns = router.urls
