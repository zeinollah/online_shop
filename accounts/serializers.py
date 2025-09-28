from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator



class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        label='Email', required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all(),
                                    message='Email already exists')]
    )

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name',
                  'email', 'password','user_role',
                  'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']
        user_role = validated_data['user_role']
        password = validated_data.pop('password')

        user = get_user_model()
        new_user = user.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_role=user_role,
        )
        new_user.set_password(password)
        new_user.save()
        return new_user



class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name','email',)


    def validate(self, attrs):
        if 'email' in attrs:
            email = attrs.get('email', None)
            query_email = get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk)

            if query_email.exists():
                raise serializers.ValidationError(
                    {"email": "This email is already in use."},
                    status.HTTP_400_BAD_REQUEST
                )

        return attrs



    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name).capitalize()
        instance.last_name = validated_data.get('last_name', instance.last_name).capitalize()
        instance.email = validated_data.get('email', instance.email)

        instance.save()
        return instance
