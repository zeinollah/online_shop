from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Product
from .serializers import (
    ProductSerializer,
    ProductUpdateSerializer,
)


class ProductViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(store=request.user.seller_profile.store)
        return Response(
            {"message": "Product data upload successfully"},
            status=status.HTTP_201_CREATED
        )



class ProductInfoViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[IsAuthenticated]

    filterset_fields = ['category', 'in_stock', 'store__city']
    search_fields = ['$name', '$description', '$store__city']
    ordering_fields = ['created_at', 'price', 'category']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(store=user.seller_profile.store)



class ProductUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    permission_classes =[IsAuthenticated,]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Product data update successfully"},
            status=status.HTTP_200_OK
        )



class ProductDeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Product delete successfully"},
            status=status.HTTP_200_OK
        )