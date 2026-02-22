from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import SellerProfile, Store
from utils.validators import (
    validate_national_code,
    validate_post_code,
    validate_birth_day,
    validate_phone_number,
    )


"""
Seller Serializers
"""
class SellerProfileSerializer(serializers.ModelSerializer):

    full_name = serializers.CharField()

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

    post_code = serializers.CharField(
        label='Post Code',
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
        post_code = attrs.get('post_code')
        if self.instance.post_code is None and post_code is None:
            raise serializers.ValidationError({
                "post_code" : "Post code is required. "
            })

        return attrs


"""
Store Serializers
"""
class StoreSerializer(serializers.ModelSerializer):
    store_phone_number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Store.objects.all(),
        message="Phone number is already in use.")]
        )
    store_name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Store.objects.all(),
        message="This Store Name is already in use.")]
        )
    city = serializers.CharField(required=True)

    class Meta:
        model = Store
        fields = [
            "seller", "store_name",
            "store_phone_number", "physical_store",
            "city", "store_address", "store_post_code",
            "is_active", "created_at", "updated_at",
        ]
        read_only_fields = [
            "seller", "is_active",
            "created_at", "updated_at",
        ]

    def validate(self, attrs):
        store_name = attrs.get('store_name')
        store_phone_number = attrs.get('store_phone_number')
        physical_store = attrs.get('physical_store', True)
        store_address = attrs.get('store_address')
        store_post_code = attrs.get('store_post_code')

        request = self.context.get('request')
        seller = request.user.seller_profile

        if not store_name or store_name.strip() == "":
            raise serializers.ValidationError({
                "store_name": "Store name is required."
            })

        validate_phone_number(store_phone_number)

        if physical_store is True:
            if not store_address or store_address.strip() == "":
                raise serializers.ValidationError({
                    "store_address": "Store address is required."
                })
            if not store_post_code or store_post_code.strip() == "":
                raise serializers.ValidationError({
                    "store_post_code": "Post code is required."
                })
            validate_post_code(store_post_code)

        if physical_store is False:
            if not seller.address:
                raise serializers.ValidationError({
                    "store_address": "Please update your profile with address first."
                })
            if not seller.post_code:
                raise serializers.ValidationError({
                    "store_post_code": "Please update your profile with post code first."
                })
            attrs['store_address'] = seller.address
            attrs['store_post_code'] = seller.post_code

        return attrs


class StoreUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "store_name", "store_phone_number",
            "physical_store",
            "city", "store_address","store_post_code",
            "is_active"
        ]
        read_only_fields = [
            "seller", "id", "created_at", "updated_at",
        ]

    def validate(self, attrs):
        store_name = attrs.get('store_name')
        store_phone_number = attrs.get('store_phone_number')
        physical_store = attrs.get('physical_store',self.instance.physical_store)
        store_address = attrs.get('store_address')
        store_post_code = attrs.get('store_post_code')
        city = attrs.get('city')

        if store_name is not None and  store_name.strip() == "":
            raise serializers.ValidationError({
                "store_name": "Store name can not be empty."
            })

        if store_name is not None:
            if Store.objects.filter(store_name=store_name).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({
                    "store_name": "This store name is already in use."
                })

        if store_phone_number is not None:
            validate_phone_number(store_phone_number)
            if Store.objects.filter(store_phone_number=store_phone_number).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError({
                    "store_phone_number": "This phone number is already in use."
                })

        if physical_store is True:
            if not store_address or store_address.strip() == "":
                raise serializers.ValidationError({
                    "store_address": "Store address can not be empty."
                })
            if not store_post_code or store_post_code.strip() == "":
                raise serializers.ValidationError({
                    "store_post_code": "Post code can not be empty."
                })
            validate_post_code(store_post_code)

        if physical_store is False:
            request = self.context.get('request')
            seller = request.user.seller_profile

            if not seller.address:
                raise serializers.ValidationError({
                    "store_address": "Please update your profile with address first."
                })
            if not seller.post_code:
                raise serializers.ValidationError({
                    "store_post_code": "Please update your profile with post code first."
                })
            attrs['store_address'] = seller.address
            attrs['store_post_code'] = seller.post_code

        if city is not None and city.strip() == "":
            raise serializers.ValidationError({
                "city": "City can not be empty."
            })

        return attrs