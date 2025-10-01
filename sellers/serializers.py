from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import SellerProfile
from utils.validators import (validate_national_code,
                              validate_post_code,
                              validate_birth_day,
                              validate_phone_number,)


class SellerProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        label='Phone number',
        validators=[UniqueValidator(
            queryset=SellerProfile.objects.all(),
            message= "This Phone Number is already in use."),
                    validate_phone_number,
        ])

    national_code = serializers.CharField(
        label='National Code',
        validators=[UniqueValidator(
            queryset=SellerProfile.objects.all(),
            message='This National Code used for verified another user.'),
                    validate_national_code,
        ])

    store_post_code = serializers.CharField(
        label='Store Post Code',
        validators=[validate_post_code],
        error_messages = {
         "required": "Post code is required."
         })

    birth_day = serializers.DateField(
        label='Birth date', required=False,
        validators=[validate_birth_day]
    )

    class Meta:
        model = SellerProfile
        fields = '__all__'
        read_only_fields = ('account', 'is_verified', 'created_at', 'updated_at')


    def validate(self, attrs):
        physical_store = attrs.get('physical_store')

        if physical_store is True:
            store_address = attrs.get('store_address')

            if not store_address or store_address.strip() == "":
                raise serializers.ValidationError({
                        "store_address" : "Store address is required. "
                })

        return attrs

