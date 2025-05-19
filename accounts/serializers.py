from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator


def create_user_name(first_name, last_name, phone_number):
    digit = phone_number[-3:]
    name = f"{first_name}.{last_name}"
    username = f"{name}.{digit}"
    return username



class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        label='Phone Number', min_length=11, max_length=11, required=True,
         validators=[UniqueValidator(queryset=get_user_model().objects.all(),
                                     message='Phone Number already exists')]
    )
    email = serializers.EmailField(
        label='Email', required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all(),
                                    message='Email already exists')]
    )

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


    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = create_user_name(validated_data['first_name'],
                                   validated_data['last_name'],
                                   validated_data['phone_number'])
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



class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name',
                  'email', 'phone_number', 'address',
                  'city', 'post_code', 'birth_day',
        )
        extra_kwargs = {
            'username': {'read_only': True}
        }


    def validate(self, attrs):
        if 'phone_number' in attrs:
            phone_number = attrs.get('phone_number', None)
            query_phone = get_user_model().objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk)

            if not phone_number.isdigit() :
                raise serializers.ValidationError(
                        "Phone Number must be digits",
                        status.HTTP_400_BAD_REQUEST)

            if len(phone_number) != 11:
                 raise serializers.ValidationError(
                        "Phone Number must be 11 digits",
                         status.HTTP_400_BAD_REQUEST)

            if query_phone.exists():
                raise serializers.ValidationError(
                    "Phone Number already exists",
                    status.HTTP_400_BAD_REQUEST)

        if 'email' in attrs:
            email = attrs.get('email')
            query_email = get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk)

            if query_email.exists():
                raise serializers.ValidationError(
                    "Email already exists",
                    status.HTTP_400_BAD_REQUEST
                )

        return attrs

    # def username_update(self, validated_data, attrs, instance):
    #     first_name = attrs.get('first_name')
    #     last_name = attrs.get('last_name')
    #     phone_number = attrs.get('phone_number')
    #     three_digits = phone_number[-3:]
    #     check_username = f"{first_name}.{last_name}.{three_digits}"
    #
    #     if instance.username != check_username:
    #         new_username = create_user_name(validated_data['first_name'],
    #                                         validated_data['last_name'],
    #                                         validated_data['phone_number'])
    #         return new_username
    #     return instance.username

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name).capitalize()
        instance.last_name = validated_data.get('last_name', instance.last_name).capitalize()
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.post_code = validated_data.get('post_code', instance.post_code)
        instance.birth_day = validated_data.get('birth_day', instance.birth_day)

        new_username = create_user_name(
            first_name=instance.first_name,
            last_name=instance.last_name,
            phone_number=instance.phone_number,
        )

        if instance.username != new_username:
            instance.username = new_username

        instance.save()
        return instance



class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id']