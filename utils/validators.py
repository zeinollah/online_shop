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


def validate_file_size(max_size=None, max_files=None):
    if max_size is None:
        """default File Size is 10 MG."""
        max_size = 10*1024*1024


    def validate(value):

        if isinstance(value, (list,tuple)):

            # Validation of number of file
            if max_files is not None and len(value) > max_files:
                raise serializers.ValidationError(
                    {"detail":f"You only can upload {max_files} files."}
                )

            # Check files size
            for file in value:
                if hasattr(file, "size") and file.size > max_size:
                    raise serializers.ValidationError(
                        {"detail" : f"{file.size} is too big,"
                                    f" maximum size allowed is {(filesizeformat(max_size))}."}
                    )

        # Validation for one file
        else:
            if hasattr(value, "size") and value.size > max_size:
                raise serializers.ValidationError(
                    {"detail" : "file size is too lagre, "
                                f" maximum size allowed is {(filesizeformat(max_size))}."}
                )

        return value

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

    if not value:
        raise serializers.ValidationError(
            {"value" : "Discount value can not be empty"}
        )

    if discount_type == 'percentage':
        if value >= 100 or value <= 0:
            raise serializers.ValidationError(
                {"Discount value" : "Discount value must be between 0 and 100."}
            )
        return int(value)

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

    if scope_type in ["all_customers_all_products", "specific_customer_all_products"]:
        if target_product:
            raise serializers.ValidationError(
                {"target_product" : f"You can not set target product for ({scope_type}) discount"}
            )

    if scope_type in ["all_customers_specific_products", "all_customers_all_products"]:
        if target_customer:
            raise serializers.ValidationError(
                {"target_customer" : f"You can not set target customer for ({scope_type}) discount"}
            )