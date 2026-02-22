from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "store_name", "phone_number",
                    "name", "city", "category",
                    "price", "in_stock",
                    "slug", "description",
                    "created_at", "updated_at"]

    list_filter = ["in_stock", "store__city",]

    search_fields = ["name", "store__store_name"]


    def city(self, obj):
        return obj.store.city
    city.short_description = "City"

    def store_name(self, obj):
        return obj.store.store_name
    store_name.short_description = "Store Name"

    def phone_number(self, obj):
        return obj.store.store_phone_number
    phone_number.short_description = "Phone Number"


admin.site.register(Product, ProductAdmin)