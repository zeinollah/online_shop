from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .models import SellerProfile
from .serializers import SellerProfileSerializer
from utils.permissions import IsProfileOwnerOrSuperuser



class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [IsProfileOwnerOrSuperuser]
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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(account=request.user)
        return Response(
            {"message": "Profile Created"},
            status=status.HTTP_201_CREATED,
        )



class SellerProfileInfoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsProfileOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return SellerProfile.objects.all()
        return SellerProfile.objects.filter(account=user)

    TO_DO : "change code to when user try to watch other user profile response be 401 "



class SellerProfileUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [IsProfileOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile Updated"},
            status=status.HTTP_200_OK
        )
