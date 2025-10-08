from rest_framework.routers import DefaultRouter
from .views import (CustomerProfileCreateViewSet,
                    CustomerProfileUpdateViewSet,
                    CustomerProfileInfoViewSet,
                    CustomerProfileDetailViewSet
                    )

router = DefaultRouter()
router.register(r'create-profiles', CustomerProfileCreateViewSet, basename='create-profiles')
router.register(r'update-profiles', CustomerProfileUpdateViewSet, basename='update-profiles')
router.register(r'info-profiles', CustomerProfileInfoViewSet, basename='info-profiles')
router.register(r'delete-profiles', CustomerProfileDetailViewSet, basename='delete-profiles')

urlpatterns = router.urls

# TODO = Add -customers- into urls and remove s from profiles