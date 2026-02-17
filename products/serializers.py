from rest_framework import serializers
from .models import Product
from utils.validators import validate_file_size


class ProductSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        validators=[validate_file_size(max_size=50 * 1024 * 1024)],
        required=False,
        allow_null=True
    )
    store_name = serializers.CharField(source="seller.store_name", required=False,)
    phone_number = serializers.CharField(source="seller.phone_number", required=False,)
    city = serializers.CharField(source="seller.city", required=False,)

    class Meta:
        model = Product
        fields = [
            "id", "seller", "slug", "name",
            "description", "price", "category",
            "in_stock", "picture",
            "phone_number", "store_name", "city",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "seller", "slug",
            "store_name", "phone_number", "picture",
            "city", "created_at", "updated_at"
        ]

    def validate(self, attrs):
        seller = self.context['request'].user.seller_profile

        """
        Profile validation data
        """
        store_name = getattr(seller, 'store_name', None)
        if store_name is None or store_name.strip() == "":
            raise serializers.ValidationError(
                {"message" : "Store name is required for upload products, please update your profile."},
            )

        phone_number = getattr(seller, 'phone_number', None)
        if phone_number is None or phone_number.strip() == "":
            raise serializers.ValidationError(
                {"message" : "Phone number is required for upload products, please update your profile."},
            )

        address = getattr(seller, 'address', None)
        store_address = getattr(seller, 'store_address', None)
        if address is None and store_address is None:
            raise serializers.ValidationError(
                {"message" : "Address is required for upload products, please update your profile."},
            )

        city = getattr(seller, 'city', None)
        if city is None or city.strip() == "":
            raise serializers.ValidationError(
                {"message" : "City name is required for upload products, please update your profile."},
            )

        """
        Product fields validation data
        """
        name = attrs.get("name")
        if not name or not name.strip():
            raise serializers.ValidationError({"message": "Product name is required."})

        description = attrs.get("description")
        if not description or not description.strip():
            raise serializers.ValidationError({"message": "Description is required."})

        price = attrs.get("price")
        if price is None:
            raise serializers.ValidationError({"message": "Price is required."})
        if price < 0:
            raise serializers.ValidationError({"message": "Price cannot be negative."})
        if price ==  0 :
            raise serializers.ValidationError({"message": "Price cannot be 0."})

        return attrs



class ProductUpdateSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        validators=[validate_file_size(max_size=50 * 1024 * 1024)],
        required=False,
        allow_null=True
    )

    class Meta:
        model = Product
        fields = [
            "name", "description", "price",
            "category", "in_stock", "picture",
            "slug"
        ]
        read_only_fields = ["slug"]

    def validate(self, attrs):
        name=attrs.get("name")
        description=attrs.get("description")
        price=attrs.get("price")


        if name is not None and name.strip() == "":
            raise serializers.ValidationError({
               "message": "Product name cannot be empty."
           })

        if description is not None and description.strip() == "":
            raise serializers.ValidationError({
                "message": "Description can not be empty."
            })

        if price is not None:
            if int(price) < 0:
                raise serializers.ValidationError({
                    "message": "Price cannot be negative."
                })
            if int(price) == 0 :
                raise serializers.ValidationError({
                    "message": "Price cannot be 0."
                })

        return attrs


