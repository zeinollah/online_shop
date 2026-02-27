from django.db import transaction
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from customers.models import Wallet, Transaction as WalletTransaction
from utils.permissions import IsOrderOwnerOrSuperuser
from .models import OrderItem
from .serializers import (
    Order, OrderSerializer,
    OrderUpdateSerializer,
    OrderItemCreateSerializer,
    OrderItemSerializer,
    OrderItemUpdateSerializer,
)



"""
Order Views 
"""
class OrderCreateViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'customer_profile'):
            return Response(
                {"message": "Complete the profile is required to create an order."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user.customer_profile)
        return Response({
            "message": "Order created."},
            status=status.HTTP_201_CREATED
        )



class OrderInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]
    filterset_fields = ['order_status', 'shipping_city', 'payment_method', 'is_paid']
    search_fields = ['order_number', 'shipping_city', 'shipping_address']
    ordering_fields = ['created_at', 'order_status']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Order.objects.all()

        if hasattr(user, 'customer_profile'):
            return Order.objects.filter(customer=user.customer_profile)

        else:
            return Order.objects.none()



class OrderUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_status = request.data.get("order_status") # Refund money to customer after canceled payd order by wallet
        if new_status == "cancelled" and instance.is_paid and instance.payment_method == "wallet":
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(customer=instance.customer)
                wallet.balance += instance.total_price
                wallet.save()

                instance.is_paid = False
                instance.paid_at = None

                WalletTransaction.objects.create(
                    wallet = wallet,
                    transaction_type = "refund",
                    amount = instance.total_price,
                    order = instance,
                )
                serializer.save()
        else:
            serializer.save()

        return Response(
            {"message": "Order updated."},
        status=status.HTTP_200_OK
        )



class OrderDeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(
            {"message": "Order deleted."},
            status=status.HTTP_200_OK
        )



"""
OrderItem Views 
"""
class OrderItemCreateViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'customer_profile'):
            return Response(
                {"message": "Complete the profile is required to create an order."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Item added to order successfully.",
                "item": serializer.data
            },
            status=status.HTTP_201_CREATED
        )



class OrderItemInfoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]
    filterset_fields = ['order__order_status', 'store_name']
    search_fields = ['product_name', 'store_name']
    ordering_fields = ['created_at', 'price', 'quantity']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return OrderItem.objects.all()

        if hasattr(user, 'customer_profile'):
            return OrderItem.objects.filter(order__customer=user.customer_profile)

        else:
            return OrderItem.objects.none()



class OrderItemUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.order.calculate_total()

        return Response(
            {"message": "Order Item updated.",
             "item" : serializer.data
        })



class OrderItemDeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        return Response(
            {"message": "Item deleted successfully."},
        )
