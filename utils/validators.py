from rest_framework import serializers
from django.template.defaultfilters import filesizeformat
from discounts.models import SellerDiscount, SiteDiscount
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
def validate_discount_usage_time(start_date, end_date):
    """
    Make sure customer can not use discount code before start date or after end date.
    """

    today = date.today()

    if today < start_date :
        raise serializers.ValidationError(
            {"Start date" :  "Discount not is available yet,"
                           f"you can use it from {start_date}"}
        )

    if today > end_date :
        raise serializers.ValidationError(
            {"End date" : f"Discount is expired on {end_date}"}
        )

    return True


def validate_discount_create_time(start_date, end_date):
    """
    Check dates to be sure admin or seller can not make discount code with wrong dates.
    """

    if start_date >= end_date :
        raise serializers.ValidationError(
            {"Date" : "End date must be after start date."}
        )

    return True


def validate_discount_value(discount_type, value):

    if discount_type == 'percentage':
        if value > 100 or value <= 0  :
            raise serializers.ValidationError(
                {"Discount value" : "Discount value must be between 0 and 100."}
            )

    if discount_type == 'fixed_amount':
        if value <= 0 :
            raise serializers.ValidationError(
                {"Discount value" : "Discount value must be greater than 0."}
            )

    return value


def validate_customer_eligibility(discount):

    scope_type = discount.scope_type

    if scope_type in ["specific_customer_all_products", "specific_customer_specific_products"]:
        if not discount.target_customer:
            raise serializers.ValidationError(
                {"target_customer" : f"Target customer must be set for this type of discount({scope_type})."}
            )

    return discount


def validate_product_eligibility(discount, order):

    target_product_id = discount.target_product.id
    target_product = discount.target_product

    eligible_items = []

    # Site Discount Check -------------------------------------------------------
    if isinstance(discount, SiteDiscount):
        if discount.scope_type in ['all_customers_specific_products', 'specific_customer_specific_products']:
            for item in order.order_items.all():
                if item.product.id == target_product_id and item not in eligible_items:
                    eligible_items.append(item)


        if discount.scope_type in ['all_customers_all_products', 'specific_customer_all_products']:
            eligible_items = list(order.order_items.all())


    # Seller Discount Check -----------------------------------------------------
    if isinstance(discount, SellerDiscount):
        seller = discount.seller

        if discount.scope_type in ['all_customers_all_products', 'specific_customer_all_products']:
            for item in order.order_items.all():
                if item.product.seller == seller:
                    eligible_items.append(item)

        if discount.scope_type in ['all_customers_specific_products', 'specific_customer_specific_products']:
            for item in order.order_items.all():
                if item.product.seller == seller and item.product.id == target_product_id:
                    eligible_items.append(item)

        if target_product:
            if seller != discount.seller :
                raise serializers.ValidationError(
                    {"target_product": f"Product ({target_product}) does not belong to your shop"}
                )



    # Check the items -----------------------------------------------------------
    elif not eligible_items:
        raise serializers.ValidationError(
           {"No items in your order are eligible for this discount"}
        )

    return eligible_items


def validate_no_overlap(discount_data, discount_id=None, ):
    pass
