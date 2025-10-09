from django.template.context_processors import request
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.permissions import IsProfileOwnerOrSuperuser
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[IsAuthenticated, IsProfileOwnerOrSuperuser]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user.seller_profile)
        return Response(
            {"message": "Product data upload successfully"},
            status=status.HTTP_201_CREATED
        )



class ProductDetailViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[IsAuthenticated, IsProfileOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Product.objects.all()
        return Product.objects.filter(seller=user.seller_profile)



class ProductUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes =[IsAuthenticated,IsProfileOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user.seller_profile)
        return Response(
            {"message": "Product data update successfully"},
        )



class ProductDeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrSuperuser]
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Product delete successfully"},
        )