from rest_framework import serializers
from utils.validators import (validate_phone_number,
                              validate_post_code,
                              validate_quantity,
                              validate_discount,
                              )
from .models import Order, OrderItem



class OrderSerializer(serializers.ModelSerializer):

    shipping_city = serializers.CharField(required=False)
    shipping_address = serializers.CharField(required=False)
    shipping_phone = serializers.CharField(
        required=False,
        validators=[validate_phone_number]
    )
    shipping_postcode = serializers.CharField(
        required=False,
        validators=[validate_post_code]
    )


    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields =(
            'id', 'customer','order_number', 'total_price',
            'created_at', 'updated_at'
        )

    def validate(self, attrs):
        """
        Get data for shipping fields from Customer Profile and validate the data.
        """
        request = self.context.get('request')
        customers = request.user.customer_profile


        if not hasattr(request.user , 'customer_profile'):
            raise serializers.ValidationError(
                {"detail": "Profile not find."},
            )

        if not attrs.get('shipping_city'):
            if customers.city:
                attrs['shipping_city'] = customers.city
            else:
                raise serializers.ValidationError(
                    {"shipping_city": "Shipping city required."
                                "Please provide it or update your profile."}
                    )

        if not attrs.get('shipping_address'):
            if customers.address:
                attrs['shipping_address'] = customers.address
            else:
                raise serializers.ValidationError(
                    {"shipping_address": "Shipping address required."
                                        "Please provide it or update your profile."}
                    )

        if not attrs.get('shipping_phone'):
            if customers.phone_number:
                attrs['shipping_phone'] = customers.phone_number
            else:
                raise serializers.ValidationError(
                     {"shipping_phone": "Shipping phone required."
                                     "Please provide it or update your profile."}
                    )

        if not attrs.get('shipping_post_code'):
            if customers.post_code:
                attrs['shipping_post_code'] = customers.post_code
            else:
                raise serializers.ValidationError(
                    {"shipping_post_code": "Shipping post code required. "
                                           "Please provide it or update your profile."}
                )

        if not attrs.get('payment_method'):
            raise serializers.ValidationError(
                {"payment_method" : "Payment method required please choose from [Cash - Wallet - Credit Card]"}
            )

        return attrs



class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id', 'customer', 'order_number', 'total_price',
            'is_paid', 'paid_at',
            'created_at', 'updated_at'
        ]


    def validate(self, attrs):

        if attrs:
            if self.instance.order_status == 'cancelled' and attrs.get('order_status') == 'cancelled':
                raise serializers.ValidationError({
                    "order_status": "Order already cancelled"
                })

            if self.instance.order_status not in ['pending', 'paid', 'processing'] and attrs.get('order_status') == 'cancelled':
                raise serializers.ValidationError({
                    "order_status": f"Order cannot be cancel in this {self.instance.order_status} status "
                                    "Only the 'pending' 'paid' and 'processing' are able to cancel"
                })

            if self.instance.order_status == 'cancelled' and attrs.get('order_status') != 'cancelled':
                raise serializers.ValidationError({
                    "order_status": "Cannot modify a cancelled order"
                })

        return attrs



class OrderItemSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source = 'order.customer')
    order_number = serializers.CharField(source = 'order.order_number')


    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = [
            'id', 'customer', 'order_number',
            'product_name', 'store_name', 'quantity', 'price',
            'discount', 'created_at', 'updated_at'
        ]



class OrderItemCreateSerializer(serializers.ModelSerializer):

    quantity = serializers.IntegerField(
        validators=[validate_quantity],
        default=1,
        )

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        read_only_fields = ['id', 'price', 'created_at', 'updated_at']

    def validate(self, attrs):
        product = attrs.get('product')
        order = attrs.get('order')

        request = self.context.get('request')
        if request and hasattr(request.user, 'customer_profile'):
            if order.customer != request.user.customer_profile:
                raise serializers.ValidationError({
                    "Order" : "You can only add order for yourself"
                })

        if not product.in_stock :
            raise serializers.ValidationError({
                "Product" : "Product not in stock."
            })


        return attrs

    def create(self, validated_data):
        products = validated_data['product']
        order = validated_data['order']

        validated_data['product_name'] = products.name
        validated_data['store_name'] = products.seller.store_name
        validated_data['price'] = products.price

        order_item = OrderItem.objects.create(**validated_data)
        order.calculate_total()
        return order_item



class OrderItemUpdateSerializer(serializers.ModelSerializer):

    quantity = serializers.CharField(
        validators=[validate_quantity],
        default=1,
        )
    discount = serializers.CharField(
        validators=[validate_discount]
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        read_only_fields = ['id', 'price', 'created_at', 'updated_at']


    def validate(self, attrs):

        order = attrs.get('order')
        product = attrs.get('product')
        discount = attrs.get('discount', self.instance.discount)
        quantity = attrs.get('quantity', self.instance.quantity)

        request = self.context.get('request')
        if request and hasattr(request.user, 'customer_profile'):
            if order.customer != request.user.customer_profile:
                raise serializers.ValidationError({
                    "Order": "You can only add order for yourself"
                })

        if order.order_status != 'pending':
            raise serializers.ValidationError({
                "status": "Cannot add item to order are not pending."
            })

        if not product.in_stock :
            raise serializers.ValidationError({
                "Product" : "Product not in stock."
            })

        item_total = self.instance.price * quantity
        if item_total < discount:
            raise serializers.ValidationError({
                "discount" : f"Discount cannot exceed item total of {item_total}."
            })

        return attrs
