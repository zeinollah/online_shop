from rest_framework import serializers
from .models import Product
from utils.validators import validate_file_size


class ProductSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(
        validators=[validate_file_size(max_size=50 * 1024 * 1024)],
        required=False,
        allow_null=True
    )
    store_name = serializers.CharField(source="store.store_name", required=False)
    store_phone_number = serializers.CharField(source="store.store_phone_number", required=False)
    city = serializers.CharField(source="store.city", required=False)

    class Meta:
        model = Product
        fields = [
            "id", "store", "slug", "name",
            "description", "price", "category",
            "in_stock", "picture",
            "store_phone_number", "store_name", "city",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "store", "slug",
            "store_name", "store_phone_number",
            "city", "created_at", "updated_at"
        ]

    def validate(self, attrs):
        seller = self.context['request'].user.seller_profile

        if not hasattr(seller, 'store'):
            raise serializers.ValidationError(
                {"message": "You need to create a store before uploading products."}
            )

        store = seller.store

        store_name = getattr(store, 'store_name', None)
        if store_name is None or store_name.strip() == "":
            raise serializers.ValidationError(
                {"message": "Store name is required for upload products, please update your store."}
            )

        store_phone_number = getattr(store, 'store_phone_number', None)
        if store_phone_number is None or store_phone_number.strip() == "":
            raise serializers.ValidationError(
                {"message": "Phone number is required for upload products, please update your store."}
            )

        store_address = getattr(store, 'store_address', None)
        if store_address is None or store_address.strip() == "":
            raise serializers.ValidationError(
                {"message": "Store address is required for upload products, please update your store."}
            )

        city = getattr(store, 'city', None)
        if city is None or city.strip() == "":
            raise serializers.ValidationError(
                {"message": "City is required for upload products, please update your store."}
            )

        store_post_code = getattr(store, 'store_post_code', None)
        if store_post_code is None or store_post_code.strip() == "":
            raise serializers.ValidationError(
                {"message": "Post code is required for upload products, please update your store."}
            )

        """
        Product fields validation
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
        if price == 0:
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


