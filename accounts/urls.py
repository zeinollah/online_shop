from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationViewSet,UpdateUserViewSet

router = DefaultRouter()
router.register(r'register', RegistrationViewSet, basename='register')
router.register(r'update', UpdateUserViewSet, basename='update')

urlpatterns = router.urls