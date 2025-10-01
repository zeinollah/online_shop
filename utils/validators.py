from rest_framework import serializers
from datetime import date



def validate_phone_number(value):
    post_stripped = value.strip()

    if post_stripped:
        if not post_stripped.isdigit():
            raise serializers.ValidationError(
                "Phone number should contain only digits."
            )
        if len(post_stripped) != 11:
            raise serializers.ValidationError(
                "Phone number should be 11 digit."
            )
    return post_stripped



def validate_national_code(value):

    if value and value.strip():
        if not value.isdigit():
            raise serializers.ValidationError(
                "national code should be digit "
            )
        if len(value) != 10:
            raise serializers.ValidationError(
                "national code should be 10 digit "
            )
    return value



def validate_post_code(value):

    stripped_value = value.strip()

    if not stripped_value:
        raise serializers.ValidationError(
            "Post code is required."
        )

    if not stripped_value.isdigit():
        raise serializers.ValidationError(
            "Post code should contain only digits."
        )

    if len(stripped_value) != 10 :
        raise serializers.ValidationError(
            "Post code should be 10 digits."
        )

    return stripped_value



def validate_birth_day(value):

    today = date.today()
    if value :
        if value == today:
            raise serializers.ValidationError(
                "birth day should be less than today"
            )
        if value > today:
            raise serializers.ValidationError(
                "birth day can not be in future"
            )
    return value



def validate_file_size(value):
    pass