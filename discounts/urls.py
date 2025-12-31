from rest_framework.routers import DefaultRouter
from .views import (SellerDiscountCreateViewSet,
                    SellerDiscountInfoViewSet,
                    )

router = DefaultRouter()
router.register('create-seller-discount', SellerDiscountCreateViewSet, basename='create_discount')
router.register('seller-discount-info', SellerDiscountInfoViewSet, basename='info_discount')
urlpatterns = router.urls
