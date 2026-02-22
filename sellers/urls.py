from rest_framework.routers import DefaultRouter
from .views import (
    SellerCreateProfileViewSet,
    SellerProfileInfoViewSet,
    SellerProfileUpdateViewSet,
    SellerProfileDeleteViewSet,
    StoreViewSet,
    StoreUpdateViewSet,
    StoreDeleteViewSet,
    StoreInfoViewSet
    )




router = DefaultRouter()

"""Seller Profile Path"""
router.register(r'create-sellers-profile', SellerCreateProfileViewSet, basename='create-sellers-profile')
router.register(r'info-sellers-profile', SellerProfileInfoViewSet, basename='info-sellers-profile')
router.register(r'update-sellers-profile', SellerProfileUpdateViewSet, basename='update-sellers-profile')
router.register(r'delete-seller-profile', SellerProfileDeleteViewSet, basename='delete-seller-profile')

"""Store Path"""
router.register(r'create-store', StoreViewSet, basename='create-store')
router.register(r'info-store', StoreInfoViewSet, basename='info-store')
router.register(r'update-store', StoreUpdateViewSet, basename='update-store')
router.register(r'delete-store', StoreDeleteViewSet, basename='delete-store')
urlpatterns = router.urls