from rest_framework import routers
from .views import CustomerProfileViewSet


router = routers.DefaultRouter()

router.register(r"customers_profile", CustomerProfileViewSet, basename="customers_profile")



urlpatterns = router.urls
