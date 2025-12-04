from rest_framework import serializers
from utils.validators import validate_phone_number, validate_post_code
from .models import Order



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


        if not hasattr(request.uesr , 'customer_profile'):
            raise serializers.ValidationError(
                {"detail": "Profile not find."},
            )

        if not attrs.get('shipping_city'):
            if customers.city:
                attrs['shipping_city'] = customers.city
            raise serializers.ValidationError(
                {"shipping_city": "Shipping city required."
                "Please provide it or update your profile."}
            )

        if not attrs.get('shipping_address'):
            if customers.address:
                attrs['shipping_address'] = customers.address
            raise serializers.ValidationError(
                {"shipping_address": "Shipping address required."
                 "Please provide it or update your profile."}
            )

        if not attrs.get('shipping_phone'):
            if customers.phone_number:
                attrs['shipping_phone'] = customers.phone_number
            raise serializers.ValidationError(
                {"shipping_phone": "Shipping phone required."
                 "Please provide it or update your profile."}
            )

        if not attrs.get('shipping_postcode'):
            if customers.post_code:
                attrs['shipping_postcode'] = customers.post_code
            raise serializers.ValidationError(
                {"shipping_postcode": "Shipping postcode required."
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