from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet,
                    ProductInfoViewSet,
                    ProductUpdateViewSet,
                    ProductDeleteViewSet
                    )

router = DefaultRouter()

router.register(r'upload-products', ProductViewSet, basename='upload_product')
router.register(r'products-info', ProductInfoViewSet, basename='product_info')
router.register(r'update-products', ProductUpdateViewSet, basename='update_product')
router.register(r'delete-products', ProductDeleteViewSet, basename='delete_product')

urlpatterns = router.urls