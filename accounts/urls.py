from rest_framework.routers import DefaultRouter
from .views import (RegistrationViewSet,
                    UserInfoViewSet,
                    UpdateUserViewSet,
                    DeleteUserViewSet)

router = DefaultRouter()
router.register(r'register', RegistrationViewSet, basename='register')
router.register(r'userinfo', UserInfoViewSet, basename='userinfo')
router.register(r'update', UpdateUserViewSet, basename='update')
router.register(r'delete', DeleteUserViewSet, basename='delete')

urlpatterns = router.urls