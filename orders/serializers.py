from operator import truediv

from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    shipping_address = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Shipping Address is required and cannot be empty.',}
    )

    shipping_post_code = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Shipping Post Code is required and cannot be empty.',}
    )

    shipping_phone = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Shipping Phone is required and cannot be empty.',}
    )

    shipping_city = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Shipping City is required and cannot be empty.',}
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields =(
            'id', 'customer','order_number',
            'created_at', 'updated_at'
        )


