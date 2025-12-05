from django.test import TestCase
from rest_framework.exceptions import ValidationError
from utils.validators import(validate_quantity,
                             validate_product,
                             validate_discount
                             )
from unittest.mock import Mock




class TestQuantityValidator(TestCase):

    def test_validate_quantity_valid(self):

        result = validate_quantity(5)
        self.assertEqual(result, 5)

    def test_validate_quantity_zero(self):
        with self.assertRaises(ValidationError) as context:
            validate_quantity(0)

        error_dict = context.exception.detail
        self.assertIn("Quantity can not be 0 or negative", str(error_dict))

    def test_validate_quantity_negative(self):
        with self.assertRaises(ValidationError) as context:
            validate_quantity(-1)

        error_dict = context.exception.detail
        self.assertIn("Quantity can not be 0 or negative", str(error_dict))



class TestProductValidator(TestCase):

    def test_validate_product_in_stock(self):
        mock_product = Mock()
        mock_product.in_stock = True

        result = validate_product(mock_product)
        self.assertEqual(result, mock_product)

    def test_validate_product_out_of_stock(self):
        mock_product = Mock()
        mock_product.in_stock = False

        with self.assertRaises(ValidationError) as context:
            validate_product(mock_product)

        error_dict = context.exception.detail
        self.assertIn("Product is not in stock", str(error_dict))



class TestDiscountValidator(TestCase):

    def test_validate_discount_valid(self):
        discount = 100
        attrs = {'total_price': 1000}

        result = validate_discount(discount, attrs)
        self.assertEqual(result, 100)

    def test_validate_discount_equals_total_price(self):
        discount = 1000
        attrs = {'total_price': 1000}

        result = validate_discount(discount, attrs)
        self.assertEqual(result, 1000)

    def test_validate_discount_negative(self):
        discount = -100
        attrs = {'total_price': 1000}

        with self.assertRaises(ValidationError) as context:
            validate_discount(discount, attrs)

        self.assertIn("Discount can not be negative", str(context.exception))

    def test_validate_discount_exceeds_total_price(self):
        discount = 1500
        attrs = {'total_price': 1000}
        with self.assertRaises(ValidationError) as context:
            validate_discount(discount, attrs)
        self.assertIn("Discount cannot exceed total price", str(context.exception))