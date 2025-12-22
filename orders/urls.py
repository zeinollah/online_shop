from rest_framework.routers import DefaultRouter
from .views import (OrderCreateViewSet,
                    OrderInfoViewSet,
                    OrderDeleteViewSet,
                    OrderUpdateViewSet,
                    OrderItemCreateViewSet,
                    OrderItemInfoViewSet,
                    OrderItemUpdateViewSet,
                    OrderItemDeleteViewSet,
                    )

router = DefaultRouter()

"""
Order urls
"""
router.register(r'order-create', OrderCreateViewSet, basename='order_create')
router.register(r'order-info', OrderInfoViewSet, basename='order_info')
router.register(r'order-delete', OrderDeleteViewSet, basename='order_detail')
router.register(r'order-update', OrderUpdateViewSet, basename='order_update')


"""
Order Item urls
"""
router.register(r'order-item-create', OrderItemCreateViewSet, basename='order_item_create')
router.register(r'order-item-info', OrderItemInfoViewSet, basename='order_item_update')
router.register(r'order-item-update', OrderItemUpdateViewSet,basename='order_item_update')
router.register(r'order-item-delete', OrderItemDeleteViewSet, basename='order_item_delete')


urlpatterns = router.urls
