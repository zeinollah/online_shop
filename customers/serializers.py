from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomerProfile
from datetime import date


class CustomerProfileSerializer(serializers.ModelSerializer):
    national_code = serializers.CharField(
        label='National Code', required=False,
        validators=[UniqueValidator(
            queryset=CustomerProfile.objects.all(),
            message='This National Code used for verified another user.')]
    )
    phone_number = serializers.CharField(
        label='Phone Number', required=True,
        validators=[UniqueValidator(
            queryset=CustomerProfile.objects.all(),
            message ='This Phone Number is already in use.')]
    )

    class Meta:
        model = CustomerProfile
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at', 'is_verified', 'account')


    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('Phone number must be an integer')
        if len(value) != 11:
            raise serializers.ValidationError('Phone number must be 11 digits')
        return value

    def validate_national_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('National Code must be an integer')
        if len(value) != 10:
            raise serializers.ValidationError('National Code must be 10 digits')
        return value

    def validate_birth_day(self, value):
        today = date.today()
        if value == today or value > today:
            raise serializers.ValidationError('Please enter a valid date')
        return value