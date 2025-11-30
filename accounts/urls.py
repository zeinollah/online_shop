from rest_framework.routers import DefaultRouter
from .views import (RegistrationViewSet,
                    UserInfoViewSet,
                    UpdateUserViewSet,
                    DeleteUserViewSet)

router = DefaultRouter()
router.register(r'register', RegistrationViewSet, basename='register')
router.register(r'userinfo', UserInfoViewSet, basename='userinfo')
router.register(r'user-update', UpdateUserViewSet, basename='user-update')
router.register(r'user-delete', DeleteUserViewSet, basename='user-delete')

urlpatterns = router.urls
