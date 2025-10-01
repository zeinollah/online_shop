from rest_framework.routers import DefaultRouter
from .views import (SellerProfileViewSet,
                    SellerProfileInfoViewSet,
                    SellerProfileUpdateViewSet,
                    SellerProfileDeleteViewSet,
                   )




router = DefaultRouter()

router.register(r'create-sellers-profile', SellerProfileViewSet, basename='create-sellers-profile')
router.register(r'info-sellers-profile', SellerProfileInfoViewSet, basename='info-sellers-profile')
router.register(r'update-sellers-profile', SellerProfileUpdateViewSet, basename='update-sellers-profile')
router.register(r'delete-seller-profile', SellerProfileDeleteViewSet, basename='delete-seller-profile')
urlpatterns = router.urls