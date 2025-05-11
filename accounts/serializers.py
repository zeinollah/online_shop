from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(label='Phone Number', min_length=11, max_length=11, required=True)
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name','username',
                  'email', 'password',
                  'phone_number', 'address',
                  'city', 'user_roll',
                  'post_code', 'birth_day',
                  'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True}
        }

    def user_name_create(self,validated_data):
        digits = validated_data.get('phone_number')
        three_digits = digits[-3:]
        name = f"{validated_data.get('first_name')}{'_'}{validated_data.get('last_name')}"
        user_name = f"{name}{'_'}{three_digits}"
        return user_name

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = self.user_name_create(validated_data)
        email = validated_data['email']
        phone_number = validated_data['phone_number']
        address = validated_data['address']
        city = validated_data['city']
        post_code = validated_data['post_code']
        user_roll = validated_data['user_roll']
        password = validated_data.pop('password')
        birth_day = validated_data['birth_day']

        user = get_user_model()
        new_user = user.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city,
            user_roll=user_roll,
            post_code=post_code,
            birth_day=birth_day,
        )
        new_user.set_password(password)
        new_user.save()
        return new_user
