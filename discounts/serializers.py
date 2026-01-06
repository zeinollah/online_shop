from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from orders.models import OrderItem
from .models import SellerDiscount, SiteDiscount, DiscountUsage
from products.models import Product
from utils.validators import (
    validate_discount_create_time,
    validate_discount_value,
    validate_scope_type,
    )


"""
Seller Discounts Serializers 
"""
class SellerDiscountListSerializer(serializers.ModelSerializer):

    seller_name = serializers.CharField(source='seller.store_name', read_only=True)
    target_customer_name = serializers.CharField(source='target_customer.full_name', read_only=True)
    target_product_name = serializers.CharField(source='target_product.name', read_only=True)

    class Meta:
        model = SellerDiscount
        fields = [
            'id', 'code', 'name', 'discount_type', 'value',
            'scope_type', 'is_active', 'is_used', 'used_at',
            'start_date', 'end_date',
            'seller_name',
            'target_product_name','target_customer_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'code', 'name', 'discount_type', 'value',
            'scope_type', 'is_active', 'is_used', 'used_at',
            'start_date', 'end_date',
            'seller_name', 'target_customer_name',
            'target_product_name',
            'created_at', 'updated_at',
        ]


class SellerDiscountCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[
        UniqueValidator(
            queryset=SellerDiscount.objects.all(),
            message='Code already exists'
        )]
    )
    class Meta:
        model = SellerDiscount
        fields = [
            'code', 'name', 'discount_type', 'value',
            'scope_type', 'is_active', 'is_used', 'used_at',
            'start_date', 'end_date',
            'used_by', 'seller', 'target_customer', 'target_product',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'seller', 'created_at', 'updated_at'
        ]

    def validate(self, attrs):

        # Use the utils/validators function ----------------------------------
        validate_discount_create_time(attrs['start_date'], attrs['end_date'])
        validate_discount_value(attrs['discount_type'], attrs['value'])
        validate_scope_type(attrs['scope_type'], attrs['target_product'], attrs['target_customer'])

        # Local Validation ---------------------------------------------------
        request = self.context.get('request')
        seller = request.user.seller_profile
        target_product = attrs.get('target_product')

        if target_product:
            if seller != target_product.seller:
                raise serializers.ValidationError(
                    {"ownership" : f"Product ({target_product.name}) dose not belong to your shop "}
                )

        return attrs


class SellerDiscountUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerDiscount
        fields = [
            'name', 'discount_type', 'value',
            'scope_type','is_active', 'start_date', 'end_date',
            'target_customer', 'target_product',
        ]
        read_only_fields = [
            'code', 'seller',
            'is_used', 'used_by', 'used_at',
            'created_at', 'updated_at',
        ]

    def validate(self, attrs):

        # Use the utils/validators function ---------------------------------
        validate_discount_create_time(attrs['start_date'], attrs['end_date'])
        validate_discount_value(attrs['discount_type'], attrs['value'])
        validate_scope_type(attrs['scope_type'], attrs['target_product'], attrs['target_customer'])

        # Local Validation --------------------------------------------------
        if self.instance.is_used:
            raise serializers.ValidationError(
                {"is_used" : "Can not updated discount code already used "}
            )

        request = self.context.get('request')
        seller = request.user.seller_profile
        target_product = attrs.get('target_product')

        if target_product:
            if seller != target_product.seller:
                raise serializers.ValidationError(
                    {"ownership" : f"Product ({target_product.name}) dose not belong to your shop "}
                )
