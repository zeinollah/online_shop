from rest_framework.routers import DefaultRouter
from .views import (
    StoreDiscountCreateViewSet,
    StoreDiscountUpdateViewSet,
    StoreDiscountInfoViewSet,
    StoreDiscountDeleteViewSet,
    SiteDiscountCreateViewSet,
    SiteDiscountInfoViewSet,
    SiteDiscountUpdateViewSet,
    SiteDiscountDeleteViewSet,
    DiscountApplyViewSet,
    DiscountUsageListViewSet,
    DiscountRemoveViewSet,
    )

router = DefaultRouter()

"""Seller Discount Urls"""
router.register('seller-discount-info', StoreDiscountInfoViewSet, basename='seller_discount_info')
router.register('create-seller-discount', StoreDiscountCreateViewSet, basename='create_seller_discount')
router.register('update-seller-discount', StoreDiscountUpdateViewSet, basename='update_seller_discount')
router.register('delete-seller-discount', StoreDiscountDeleteViewSet, basename='delete_seller_discount')


"""Site Discount Urls"""
router.register('site-discount-info', SiteDiscountInfoViewSet, basename='site_discount_info')
router.register('create-site-discount', SiteDiscountCreateViewSet, basename='create_site_discount')
router.register('update-site-discount', SiteDiscountUpdateViewSet, basename='update_site_discount')
router.register('delete-site-discount', SiteDiscountDeleteViewSet, basename='delete_site_discount')


"""Discount Usage Urls"""
router.register('discount-usage', DiscountUsageListViewSet, basename='discount_usage')
router.register('apply-discount', DiscountApplyViewSet, basename='apply_discount')
router.register('delete-discount', DiscountRemoveViewSet, basename='delete_discount')


urlpatterns = router.urls
