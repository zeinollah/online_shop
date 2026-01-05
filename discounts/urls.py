from rest_framework.routers import DefaultRouter
from .views import (
    SellerDiscountCreateViewSet,
    SellerDiscountUpdateViewSet,
    SellerDiscountInfoViewSet,
    SellerDiscountDeleteViewSet,
    )

router = DefaultRouter()

router.register('seller-discount-info', SellerDiscountInfoViewSet, basename='seller_discount_info')
router.register('create-seller-discount', SellerDiscountCreateViewSet, basename='create_seller_discount')
router.register('update-seller-discount', SellerDiscountUpdateViewSet, basename='update_seller_discount')
router.register('delete-seller-discount', SellerDiscountDeleteViewSet, basename='delete_seller_discount')

urlpatterns = router.urls
