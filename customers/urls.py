from rest_framework.routers import DefaultRouter
from .views import (CustomerProfileCreateViewSet,
                    CustomerProfileUpdateViewSet,
                    CustomerProfileInfoViewSet,
                    )

router = DefaultRouter()
router.register(r'create-profiles', CustomerProfileCreateViewSet, basename='create-profiles')
router.register(r'update-profiles', CustomerProfileUpdateViewSet, basename='update-profiles')
router.register(r'info-profiles', CustomerProfileInfoViewSet, basename='info-profiles')

urlpatterns = router.urls