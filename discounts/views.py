from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.permissions import IsDiscountOwnerOrSuperuser
from .models import SellerDiscount, SiteDiscount
from .serializers import (
    SellerDiscountListSerializer,
    SellerDiscountCreateSerializer,
    SellerDiscountUpdateSerializer, SiteDiscountCreateSerializer,
)



"""
Seller Discount Views 
"""
class SellerDiscountCreateViewSet(viewsets.ModelViewSet):
    queryset = SellerDiscount.objects.all()
    serializer_class = SellerDiscountCreateSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'seller_profile'):
            return Response(
                {"message": "Complete the profile is required to create Discount code."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user.seller_profile)

        return Response({
            "message": "Your Discount has been created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class SellerDiscountInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SellerDiscount.objects.all()
    serializer_class = SellerDiscountListSerializer
    permission_classes = [IsAuthenticated, IsDiscountOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return SellerDiscount.objects.all()

        if hasattr(user, 'seller_profile'):
            return SellerDiscount.objects.filter(seller=user.seller_profile)

        else:
            return False


class SellerDiscountUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SellerDiscount.objects.all()
    serializer_class = SellerDiscountUpdateSerializer
    permission_classes = [IsAuthenticated, IsDiscountOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Your Discount has been updated successfully",
            "data": serializer.data},
            status=status.HTTP_200_OK
        )


class SellerDiscountDeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SellerDiscount.objects.all()
    serializer_class = SellerDiscountUpdateSerializer
    permission_classes = [IsAuthenticated, IsDiscountOwnerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Your Discount has been deleted successfully",
        })



"""
Site Discount Views
"""
class SiteDiscountCreateViewSet(viewsets.ModelViewSet):
    queryset = SiteDiscount.objects.all()
    serializer_class = SiteDiscountCreateSerializer
    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return Response(
                {"message" : "Only Admin can create site discounts"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Your Discount has been created successfully",
            "data": serializer.data
        },
             status=status.HTTP_201_CREATED
        )
