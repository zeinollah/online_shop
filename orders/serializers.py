from rest_framework import serializers, validators
from .models import Order, OrderItem



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



class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id', 'customer', 'order_number',
            'total_price', 'is_paid', 'paid_at',
            'created_at', 'updated_at'
        ]


    def validate(self, attrs):

        if self.instance.order_status == 'cancelled' and attrs.get('order_status') == 'cancelled':
            raise serializers.ValidationError({
                "order_status":"Order already cancelled"
            })

        if not self.instance.order_status in ['pending', 'paid', 'processing'] and attrs.get('order_status') == 'cancelled':
            raise serializers.ValidationError({
                "order_status":f"Order cannot be cancel in this {self.instance.order_status} status "
                                 "Only the 'pending' 'paid' and 'processing' are able to cancel"
            })

        if self.instance.order_status == 'cancelled' and attrs.get('order_status') != 'cancelled':
            raise serializers.ValidationError({
                "order_status": "You cannot change the order cancelled"
            })