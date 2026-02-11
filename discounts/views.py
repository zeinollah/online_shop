from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework.response import Response
from utils.permissions import IsDiscountOwnerOrSuperuser
from .models import SellerDiscount, SiteDiscount, DiscountUsage
from rest_framework.exceptions import PermissionDenied
from .serializers import (
    SellerDiscountListSerializer,
    SellerDiscountCreateSerializer,
    SellerDiscountUpdateSerializer,
    SiteDiscountCreateSerializer,
    SiteDiscountListSerializer,
    SiteDiscountUpdateSerializer,
    DiscountApplySerializer,
    DiscountUsageListSerializer,
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


class SiteDiscountInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteDiscount.objects.all()
    serializer_class = SiteDiscountListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return SiteDiscount.objects.all()
        else:
            raise PermissionDenied


class SiteDiscountUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SiteDiscount.objects.all()
    serializer_class = SiteDiscountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return Response(
                {"message" : "Only Admin can update site discounts"},
                status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Your Discount has been updated successfully",
            "data": serializer.data},
            status=status.HTTP_200_OK
        )


class SiteDiscountDeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SiteDiscount.objects.all()
    serializer_class = SiteDiscountUpdateSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            return Response(
                {"message" : "Only Admin can delete site discounts"},
                status=status.HTTP_403_FORBIDDEN

            )
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Your Discount has been deleted successfully"},
            status=status.HTTP_200_OK
        )


"""
Usage Discount views
"""
class DiscountUsageListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiscountUsage.objects.all()
    serializer_class = DiscountUsageListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return DiscountUsage.objects.all()

class DiscountApplyViewSet(viewsets.GenericViewSet):
    serializer_class = DiscountApplySerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'customer_profile'):
            return Response(
                {"message" : "Customer profile required"},
                        status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        discount = serializer.validated_data['discount']
        order_item = serializer.validated_data['order_item']
        customer = serializer.validated_data['customer']

        item_subtotal = order_item.price * order_item.quantity

        if discount.discount_type == 'percentage':
            discount_amount = (item_subtotal * int(discount.value)) / 100
        else:
            discount_amount = min(discount.value, item_subtotal)

        discount_usage = DiscountUsage.objects.create(
            seller_discount = discount if isinstance(discount, SellerDiscount) else None,
            site_discount = discount if isinstance(discount, SiteDiscount) else None,
            discount_code = discount.code,
            discount_type = discount.discount_type,
            discount_value = discount.value,
            customer = customer,
            order = order_item.order,
            order_item = order_item,
            discount_amount = discount_amount,
        )

        order_item.discount = discount_amount
        order_item.save()

        discount.is_used = True
        discount.used_by = customer
        discount.save()

        order_item.order.calculate_total()

        return Response({
            "message": "Discount applied successfully.",
            "discount_code": discount_usage.discount_code,
            "discount_amount": str(discount_usage.discount_amount),
            "order_item_id": discount_usage.order_item.id,
            "new_subtotal": str(order_item.subtotal)
            },
            status=status.HTTP_200_OK
        )