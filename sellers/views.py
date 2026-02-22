from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SellerProfile, Store
from .serializers import SellerProfileSerializer, StoreSerializer, StoreUpdateSerializer
from utils.permissions import IsSellerProfileOwnerOrSuperuser, IsStoreOwnerOrSuperuser


"""
Seller Profile Views
"""
class SellerCreateProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"message": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if hasattr(request.user,'seller_profile'):
            return Response(
                {"message": "Profile already created"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=request.user)
        return Response(
            {"message": "Profile Created"},
            status=status.HTTP_201_CREATED,
        )



class SellerProfileInfoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated,IsSellerProfileOwnerOrSuperuser]
    filterset_fields = ['city', 'physical_store', 'is_verified']
    search_fields = ['$account__email', 'city', '$store_name']
    ordering_fields = ['created_at', 'store_name']


    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return SellerProfile.objects.all()
        return SellerProfile.objects.filter(account=user)



class SellerProfileUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated,IsSellerProfileOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile Updated"},
            status=status.HTTP_200_OK
        )



class SellerProfileDeleteViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated,IsSellerProfileOwnerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Profile Deleted"},
            status=status.HTTP_200_OK
        )



"""
Store Views
"""
class StoreViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not hasattr(request.user, "seller_profile"):
            return Response(
                {"message": "Profile required to create store"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        seller = request.user.seller_profile
        if hasattr(seller,'store'):
            return Response(
                {"message": "You already have store"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=seller)
        return Response(
            {"message": "Store Created"},
            status=status.HTTP_201_CREATED
        )


class StoreUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreUpdateSerializer
    permission_classes = [IsAuthenticated, IsStoreOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Store Updated"},
            status=status.HTTP_200_OK
        )



class StoreInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated,IsStoreOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Store.objects.all()
        return Store.objects.filter(seller=user.seller_profile)



class StoreDeleteViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated,IsStoreOwnerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Store Deleted"},
            status=status.HTTP_200_OK
        )