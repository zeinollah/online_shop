from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomerProfile


class CustomerSerializer(serializers.ModelSerializer):
    national_code = serializers.CharField(
        label='National Code', min_length =10, required=True,
        validators=[UniqueValidator(
            queryset=CustomerProfile.objects.all(),
        message='This National Code used for verified another user.')]
    )

    class Meta:
        model = CustomerProfile
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at', 'is_verified', 'account')

    def create(self, validated_data):
        pass
    #     profile_avatar = validated_data('profile_avatar')
    #     gender = validated_data('gender')
    #     national_code = validated_data('national_code')
    #     id_card_picture = validated_data('id_card_picture')
    #     is_verified = validated_data('is_verified')
    #     city = validated_data('city')