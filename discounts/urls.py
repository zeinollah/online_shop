from rest_framework.routers import DefaultRouter
from .views import (
    SellerDiscountCreateViewSet,
    SellerDiscountUpdateViewSet,
    SellerDiscountInfoViewSet,
    SellerDiscountDeleteViewSet,
    SiteDiscountCreateViewSet,
    SiteDiscountInfoViewSet,
    SiteDiscountUpdateViewSet,
    SiteDiscountDeleteViewSet,
    DiscountApplyViewSet,
    )

router = DefaultRouter()
"""Seller Discount Urls"""
router.register('seller-discount-info', SellerDiscountInfoViewSet, basename='seller_discount_info')
router.register('create-seller-discount', SellerDiscountCreateViewSet, basename='create_seller_discount')
router.register('update-seller-discount', SellerDiscountUpdateViewSet, basename='update_seller_discount')
router.register('delete-seller-discount', SellerDiscountDeleteViewSet, basename='delete_seller_discount')

"""Site Discount Urls"""
router.register('site-discount-info', SiteDiscountInfoViewSet, basename='site_discount_info')
router.register('create-site-discount', SiteDiscountCreateViewSet, basename='create_site_discount')
router.register('update-site-discount', SiteDiscountUpdateViewSet, basename='update_site_discount')
router.register('delete-site-discount', SiteDiscountDeleteViewSet, basename='delete_site_discount')

"""Discount Usage Urls"""
router.register('apply-discount', DiscountApplyViewSet, basename='apply_discount')


urlpatterns = router.urls
