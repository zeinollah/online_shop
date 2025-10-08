from rest_framework import serializers
from django.template.defaultfilters import filesizeformat
from datetime import date



def validate_phone_number(value):
    post_stripped = value.strip()

    if post_stripped:
        if not post_stripped.isdigit():
            raise serializers.ValidationError(
                "Phone number should be digits."
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
                "national code should be digit. "
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
            "Post code should be digits."
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
                "birth day should be less than today."
            )
        if value > today:
            raise serializers.ValidationError(
                "Date in future is not valid."
            )
    return value



def validate_file_size(max_size=None, amount=None):
    if max_size is None:
        """default File Size is 20 MG."""
        max_size = 20*1024*1024

    if amount is None:
        amount = 1

    def validate(values):

        # if len(values) > amount:
        #     raise serializers.ValidationError(
        #         {f"you can only upload {amount} pictures."}
        #     )

        for value in values:
            if value.size > max_size:
                raise serializers.ValidationError(
                    f"{value.name} is too big. Maximum allowed is {filesizeformat(max_size)}, "
                    f"but it is {filesizeformat(value.size)}."
                )

        return values

    return validate