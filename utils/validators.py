from rest_framework import serializers
from django.template.defaultfilters import filesizeformat
from datetime import date




"""
Validation of Profile fields 
"""
def validate_phone_number(value):
    phone_number = value.strip()

    if phone_number:

        if not phone_number.isdigit():
            raise serializers.ValidationError(
                "Phone number should be digits."
            )
        if len(phone_number) != 11:
            raise serializers.ValidationError(
                "Phone number should be 11 digit."
            )
    return phone_number


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



"""
Validation fields need for Order
"""
def validate_quantity(value):
    value = int(value)
    if value <= 0 :
        raise serializers.ValidationError(
            {"quantity" : "Quantity can not be 0 or negative."}
        )
    return value


def validate_product(value):
    if not value.in_stock:
        raise serializers.ValidationError(
            {"product" : "Product is not in stock."}
        )
    return value


def validate_discount(value, attrs):

        if value < 0 :
            raise serializers.ValidationError(
                "Discount can not be negative."
            )
        return value



"""
Validation Discount fields
"""
def validate_discount_create_time(start_date, end_date):
    """
    Check dates to be sure admin or seller can not make discount code with wrong dates.
    """
    today = date.today()

    if start_date > end_date:
        raise serializers.ValidationError(
            {"Date" : "End Date can not before start date"}
        )

    if start_date < today:
        raise serializers.ValidationError(
            {"Date" : "Start Date can not be less than today."}
        )

    return True


def validate_discount_value(discount_type, value):

    if discount_type == 'percentage':
        if value >= 100 or value <= 0:
            raise serializers.ValidationError(
                {"Discount value" : "Discount value must be between 0 and 100."}
            )

    if discount_type == 'fixed_amount':
        if value <= 0 :
            raise serializers.ValidationError(
                {"Discount value" : "Discount value must be greater than 0."}
            )

    return value


def validate_scope_type(scope_type, target_product, target_customer):

    if scope_type in ['all_customers_specific_products', 'specific_customer_specific_products']:
        if not target_product:
            raise serializers.ValidationError(
                {"target_product" : f"Target product must set for ({scope_type})"}
            )

    if scope_type in ['specific_customer_all_products', 'specific_customer_specific_products']:
        if not target_customer:
            raise serializers.ValidationError(
                {"target_customer" : f"Target customer must set for ({scope_type})"}
            )