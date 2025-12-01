from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.permissions import IsOrderOwnerOrSuperuser
from .serializers import Order, OrderSerializer, OrderUpdateSerializer


class OrderCreateViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, 'customer.profile'):
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

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Order.objects.all()

        if hasattr(user, 'customer_profile'):
            return Order.objects.filter(customer=user.customer_profile)

        return False



class OrderUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated,IsOrderOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
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