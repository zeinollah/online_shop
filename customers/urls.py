from rest_framework.routers import DefaultRouter
from .views import (
    CustomerProfileCreateViewSet,
    CustomerProfileUpdateViewSet,
    CustomerProfileInfoViewSet,
    CustomerProfileDetailViewSet,
    WalletInfoViewSet,
    TransactionCreateViewSet,
    TransactionHistoryViewSet,
    )

router = DefaultRouter()

"""Customer Path"""
router.register(r'create-profiles', CustomerProfileCreateViewSet, basename='create-profiles')
router.register(r'update-profiles', CustomerProfileUpdateViewSet, basename='update-profiles')
router.register(r'info-profiles', CustomerProfileInfoViewSet, basename='info-profiles')
router.register(r'delete-profiles', CustomerProfileDetailViewSet, basename='delete-profiles')

"""Wallet Path"""
router.register(r'wallet-info', WalletInfoViewSet, basename='wallet-info')
router.register(r'transactions', TransactionCreateViewSet, basename='transactions')
router.register(r'transactions-history', TransactionHistoryViewSet, basename='transactions-history')
urlpatterns = router.urls

# TODO = Add -customers- into urls and remove s from profiles