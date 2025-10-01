from rest_framework.routers import DefaultRouter
from .views import (SellerProfileViewSet,
                    SellerProfileInfoViewSet,
                   )




router = DefaultRouter()

router.register(r'create-sellers-profile', SellerProfileViewSet, basename='create-sellers-profile')
router.register(r'info-sellers-profile', SellerProfileInfoViewSet, basename='info-sellers-profile')

urlpatterns = router.urls