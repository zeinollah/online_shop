from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from customers.models import CustomerProfile
from orders.models import OrderItem
from .models import SellerDiscount, SiteDiscount, DiscountUsage
from products.models import Product
from datetime import date
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
    used_by_name = serializers.CharField(source='used_by.full_name', read_only=True)

    class Meta:
        model = SellerDiscount
        fields = [
            'id', 'code', 'name', 'discount_type', 'value',
            'scope_type', 'is_active', 'is_used', 'used_by', 'used_by_name', 'used_at',
            'start_date', 'end_date',
            'seller_name',
            'target_product_name', 'target_customer_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'code', 'name', 'discount_type', 'value',
            'scope_type', 'is_active', 'is_used', 'used_by', 'used_by_name', 'used_at',
            'start_date', 'end_date',
            'seller_name',
            'target_product_name', 'target_customer_name',
            'created_at', 'updated_at'
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
            'scope_type', 'is_active',
            'start_date', 'end_date',
            'seller', 'target_customer', 'target_product',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'seller', 'created_at', 'updated_at'
        ]

    def validate(self, attrs):

        # Use the utils/validators function ----------------------------------
        validate_discount_create_time(attrs['start_date'], attrs['end_date'])
        validate_discount_value(attrs['discount_type'], attrs['value'])
        validate_scope_type(attrs['scope_type'], attrs.get('target_product'), attrs.get('target_customer'))

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
        discount_type = attrs.get('discount_type', self.instance.discount_type)
        value = attrs.get('value', self.instance.value)
        validate_discount_value(discount_type, value)

        start_date = attrs.get('start_date', self.instance.start_date)
        end_date = attrs.get('end_date', self.instance.end_date)
        validate_discount_create_time(start_date, end_date)

        scope_type = attrs.get('scope_type', self.instance.scope_type)
        target_customer = attrs.get('target_customer', self.instance.target_customer)
        target_product = attrs.get('target_product', self.instance.target_product)
        validate_scope_type(scope_type, target_product, target_customer)

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

        return attrs



"""
Site Discount Serializers
"""
class SiteDiscountListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='target_customer.full_name', read_only=True)
    product_name = serializers.CharField(source='target_product.name', read_only=True)
    used_by_name = serializers.CharField(source='used_by.full_name', read_only=True)

    class Meta:
        model = SiteDiscount
        fields = [
            'id', 'code', 'name', 'discount_type', 'scope_type',
            'value', 'is_active', 'start_date', 'end_date',
            'is_used', 'used_by_name', 'used_at',
            'target_customer', 'customer_name',
            'target_product', 'product_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'code', 'name', 'discount_type', 'scope_type',
            'value', 'is_active', 'start_date', 'end_date',
            'is_used', 'used_by_name', 'used_at',
            'target_customer', 'customer_name',
            'target_product', 'product_name',
            'created_at', 'updated_at'
        ]


class SiteDiscountCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[
        UniqueValidator(
            queryset=SiteDiscount.objects.all(),
            message='Code already exists'
        )
    ])

    class Meta:
          model = SiteDiscount
          fields = [
                "code", "name", "discount_type", "value",
                "scope_type", "start_date",
                "end_date", "is_active",
                "target_customer", "target_product",
          ]
          read_only_fields = [
             "created_at", "updated_at"
          ]



    def validate(self, attrs=None):

        # Use the utils/validators function ----------------------------------
        validate_discount_create_time(attrs['start_date'], attrs['end_date'])
        validate_discount_value(attrs['discount_type'], attrs['value'])
        validate_scope_type(attrs['scope_type'], attrs.get('target_product'), attrs.get('target_customer'))

        return attrs


class SiteDiscountUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteDiscount
        fields = [
            'name', 'discount_type', 'value',
            'is_active', 'start_date', 'end_date', 'scope_type',
            'target_customer', 'target_product'
        ]
        read_only_fields = [
            'code',
            'is_used', 'used_by', 'used_at',
            'created_at', 'updated_at'
        ]

    def validate(self, attrs):

        # Use the utils/validators function ----------------------------------
        discount_type = attrs.get('discount_type', self.instance.discount_type)
        value = attrs.get('value', self.instance.value)
        validate_discount_value(discount_type, value)

        start_date = attrs.get('start_date', self.instance.start_date)
        end_date = attrs.get('end_date', self.instance.end_date)
        validate_discount_create_time(start_date, end_date)

        scope_type = attrs.get('scope_type', self.instance.scope_type)
        target_customer = attrs.get('target_customer', self.instance.target_customer)
        target_product = attrs.get('target_product', self.instance.target_product)
        validate_scope_type(scope_type, target_product, target_customer)

        # Local Validation ---------------------------------------------------
        if self.instance.is_used:
            raise serializers.ValidationError(
                {"is_used" : "Can not updated discount code already used "}
            )

        return attrs



"""
Discount Usage Serializers
"""
class DiscountApplySerializer(serializers.Serializer):
    discount_code = serializers.CharField()
    order_item_id = serializers.IntegerField()

    def validate_discount_code(self, value):

        discount_code = SiteDiscount.objects.filter(code=value).first() # Site Discount Code Validation
        if discount_code:
            return discount_code

        discount_code = SellerDiscount.objects.filter(code=value).first() # Seller Discount Code Validation
        if discount_code:
            return discount_code

        raise serializers.ValidationError({
            "discount_code" : "Discount code does not exist"
        })

    def validate_order_item_id(self, value):

        try:
            order_item= OrderItem.objects.get(id=value)
            return order_item
        except OrderItem.DoesNotExist:
            raise serializers.ValidationError({
                "order_item_id" : "OrderItem does not exist"
            })


    def validate(self, attrs):
        discount = attrs['discount_code']
        order_item = attrs['order_item_id']
        request = self.context.get('request')
        customer = request.user.customer_profile
        product = order_item.product

        if order_item.order.customer != customer:
            raise serializers.ValidationError({
                "order_item" : "You can only apply discounts to your own orders"
            })

        if order_item.order.order_status != 'pending':
            raise serializers.ValidationError({
                "order_status" : "You can only apply discount to pending orders"
            })

        existing_discount = DiscountUsage.objects.filter(order_item=order_item).first()
        if existing_discount:
            raise serializers.ValidationError({
                "exist_code" : f"This item already has discount code applied ({existing_discount})"
            })

        if not discount.is_active :
            raise serializers.ValidationError({
                "discount" : "This discount is not active"
            })

        if discount.is_used:
            raise serializers.ValidationError({
                "discount" : "Discount already used"
            })

        today = date.today()
        if discount.start_date > today:
            raise serializers.ValidationError({
                "start_date" : f"Discount is not available yet, you can use it from {discount.start_date}"
            })

        if discount.end_date < today:
            raise serializers.ValidationError({
                "end_date" : f"Discount expired on {discount.end_date}"
            })

        scope_type = discount.scope_type
        if 'specific_customer' in scope_type:
           if discount.target_customer != customer:
               raise serializers.ValidationError({
                   "discount" : "This discount code is not available for your account"
           })

        if isinstance(discount, SiteDiscount):
            if 'specific_products' in scope_type:
                if product.id != discount.target_product.id:
                    raise serializers.ValidationError({
                        "discount": "This discount does not apply to this product."
                    })

        if isinstance(discount, SellerDiscount):

            if discount.seller != product.seller:
                raise serializers.ValidationError({
                    "discount" : "This discount does not apply to this seller."
                })

            if 'specific_products' in scope_type:
                if product.id != discount.target_product.id:
                    raise serializers.ValidationError({
                        "discount": "This discount does not apply to this product."
                    })


        attrs['discount'] = discount
        attrs['order_item'] = order_item
        attrs['customer'] = customer

        return attrs

