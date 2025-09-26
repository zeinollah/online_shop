from rest_framework import viewsets, status, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.permissions import IsProfileOwnerOrSuperuser
from .models import CustomerProfile
from .serializers import (CustomerProfileSerializer,
                          CustomerProfileUpdateSerializer,)




class CustomerProfileCreateViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, 'customer_profile'):
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


class CustomerProfileUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileUpdateSerializer
    permission_classes =[IsProfileOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile updated successfully"},
            status=status.HTTP_200_OK
        )
