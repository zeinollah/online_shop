from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.permissions import IsCustomerProfileOwnerOrSuperuser
from .models import CustomerProfile, Wallet, Transaction
from .serializers import (
    CustomerProfileSerializer,
    CustomerProfileUpdateSerializer,
    WalletInfoSerializer,
    TransactionCreateSerializer,
    )




"""
Customer Profile Views
"""
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



class CustomerProfileInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated,IsCustomerProfileOwnerOrSuperuser]
    filterset_fields = ['city', 'gender', 'is_verified']
    search_fields = ['$account__email', 'account__first_name', 'account__last_name', 'phone_number']
    ordering_fields = ['created_at', 'city', 'gender']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return CustomerProfile.objects.all()
        return CustomerProfile.objects.filter(account=user)



class CustomerProfileUpdateViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileUpdateSerializer
    permission_classes = [IsAuthenticated,IsCustomerProfileOwnerOrSuperuser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Profile updated successfully"},
            status=status.HTTP_200_OK
        )



class CustomerProfileDetailViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated,IsCustomerProfileOwnerOrSuperuser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            "message: Profile deleted successfully",
            status=status.HTTP_200_OK
        )



"""
Wallet Views
"""

class WalletInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Wallet.objects.all()
        return Wallet.objects.filter(customer=user.customer_profile)



class TransactionCreateViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        wallet = request.user.customer_profile.wallets
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction = serializer.save(wallet=wallet)

        if transaction.transaction_type == "top_up":
            wallet.balance += transaction.amount

        elif transaction.transaction_type == "payment":
            wallet.balance -= transaction.amount

        wallet.save()

        return Response(
            {"message": "Transaction completed successfully"},
            status=status.HTTP_201_CREATED
        )



class TransactionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(wallet=user.customer_profile.wallets).order_by("-created_at")
