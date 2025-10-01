from django.contrib import admin
from .models import SellerProfile

class SellerProfileAdmin(admin.ModelAdmin):
    list_display =["id", "full_name", "email",
                   "phone_number", "city", "store_name", "physical_store", "store_address",
                   "store_post_code", "is_active", "is_verified",
                   "created_at", "updated_at"
                   ]

    list_filter = ["city", "physical_store", "is_verified"]

    search_fields = ["account__first_name", "account__last_name",
                     "account__name", "store_name"
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