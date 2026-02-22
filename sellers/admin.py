from django.contrib import admin
from .models import SellerProfile, Store

class SellerProfileAdmin(admin.ModelAdmin):
    list_display =["id", "full_name", "email",
                   "phone_number", "city",
                   "post_code", "is_active", "is_verified",
                   "created_at", "updated_at"
                   ]

    list_filter = ["city", "is_verified"]

    search_fields = [
        "phone_number", "post_code",
    ]

    def email(self, obj):
        return obj.account.email
    email.admin_order_field = 'email'

    def full_name(self, obj):
        return f"{obj.account.first_name} {obj.account.last_name}"
    full_name.admin_order_field = 'first_name'

    def is_active(self, obj):
        return obj.account.is_active
    is_active.boolean = True
    is_active.admin_order_field = 'is_active'

admin.site.register(SellerProfile, SellerProfileAdmin)


class StoreAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "seller", "store_name",
        "store_phone_number",
        "physical_store",
        "store_address", "store_post_code",
        "is_active",
        "created_at", "updated_at"
    ]

    list_filter = [
        "physical_store", "city", "is_active"
    ]

    search_fields = [
        "store_name", "store_phone_number", "store_post_code"
    ]

admin.site.register(Store, StoreAdmin)