from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import SellerDiscount, SiteDiscount, DiscountUsage
from utils.validators import (
    validate_discount,
    validate_discount_usage_time,
    validate_discount_create_time,
    validate_discount_value,
    validate_customer_eligibility,
    validate_product_eligibility,
    validate_no_overlap,
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

    code = serializers.CharField(
        validators=[UniqueValidator(
            queryset=SellerDiscount.objects.all(),
        message= "This code is already exist."
        )]
    )


    class Meta:
        model = SellerDiscount
        fields = [
            'code', 'name', 'discount_type', 'value',
            'scope_type', 'is_active',
            'start_date', 'end_date',
            'target_customer', 'target_product'
        ]
        read_only_fields = ['seller', 'created_at', 'updated_at']

    def validate(self, attrs):

        # Use validation function from utils/validators.py
        validate_discount_value(attrs['discount_type'], attrs['value'])
        validate_discount_create_time(attrs['start_date'], attrs['end_date'])


        # validation of product --------------------------------------------------------------
        request = self.context.get('request')
        seller = request.user.seller_profile
        target_product = attrs.get('target_product')

        if target_product:
            if seller != target_product.seller:
                raise serializers.ValidationError(
                    {"target_product": f"Product ({target_product}) does not belong to your shop"}
                )

        return attrs



class SellerDiscountUpdateSerializer(serializers.ModelSerializer):
    pass



"""
Site Discounts Serializers 
"""
class SiteDiscountListSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(source='target_customer.full_name', read_only=True)
    product_name = serializers.CharField(source='target_product.name', read_only=True)

    class Meta:
        model = SiteDiscount
        fields = [
            'code', 'name', 'discount_type', 'scope_type',
            'value', 'is_active', 'start_date', 'end_date',
            'is_used', 'used_at', 'target_customer', 'target_product',
            'created_at', 'updated_at'
        ]

    read_only_fields = [
            'code', 'name', 'discount_type', 'scope_type',
            'value', 'is_active', 'start_date', 'end_date',
            'is_used', 'used_at', 'target_customer', 'target_product',
            'created_at', 'updated_at'
        ]



class SiteDiscountCreateSerializer(serializers.ModelSerializer):
    pass



class SiteDiscountUpdateSerializer(serializers.ModelSerializer):
    pass



"""
Discount Usage Serializers 
"""
class DiscountApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = DiscountUsage
        fields = '__all__'


    def validate_order_eligibility(self):
        ...

    # def validate_customer_eligibility(self, attrs):
    #     discount = attrs.get('discount')
    #     if discount.scope_type in ['specific_customer_all_products', 'specific_customer_specific_products']:
    #         if discount.target_customer != customer

    def validate_product_eligibility(self):
        ...

    def validate_discount_not_used(self):
        ...

    def validate_discount_usage_time(self):
        ...

    def validate_code_exist(self):
        ...

    # if  not is_active:
    #     raise serializers.ValidationError(
    #         {"is active" : "This discount code is not active"}
    #     )


class DiscountRemoveSerializer(serializers.ModelSerializer):
    pass


class DiscountUsageListSerializer(serializers.ModelSerializer):
    pass

