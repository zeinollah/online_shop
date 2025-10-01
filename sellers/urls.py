from rest_framework.routers import DefaultRouter
from .views import (SellerProfileViewSet,
                   )




router = DefaultRouter()

router.register(r'create-sellers-profile', SellerProfileViewSet, basename='create-sellers-profile')

urlpatterns = router.urls