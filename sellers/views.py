from rest_framework import viewsets, status,mixins
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