from rest_framework.routers import DefaultRouter
from .views import (OrderCreateViewSet,
                    OrderInfoViewSet,
                    OrderDeleteViewSet,
                    OrderUpdateViewSet
                    )

router = DefaultRouter()
router.register(r'orders-create', OrderCreateViewSet, basename='order_create')
router.register(r'order-info', OrderInfoViewSet, basename='order_info')
router.register(r'order-delete', OrderDeleteViewSet, basename='order_detail')
router.register(r'order-update', OrderUpdateViewSet, basename='order_update')