from rest_framework.routers import DefaultRouter
from .views import (CustomerProfileCreateViewSet,
                    CustomerProfileUpdateViewSet,
                    )

router = DefaultRouter()
router.register(r'create-profiles', CustomerProfileCreateViewSet, basename='create-profiles')
router.register(r'update-profiles', CustomerProfileUpdateViewSet, basename='update-profiles')

urlpatterns = router.urls