from django.contrib import admin
from .models import (
    StoreDiscount,
    SiteDiscount,
    DiscountUsage,
)


class StoreDiscountAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'store_name',
        'scope_type', 'discount_type', 'value',
        'is_active', 'is_used', 'used_at', 'used_by',
        'start_date', 'end_date',
        'target_product', 'target_customer'
    ]

    list_filter = [
        'store',
        'scope_type', 'discount_type',
        'is_used', 'is_active',
    ]

    search_fields = [
        'code', 'name', 'store__store_name',
    ]

    def store_name(self, obj):
        return f"{obj.store.store_name}"
    store_name.admin_order_field = 'store__store_name'

admin.site.register(StoreDiscount, StoreDiscountAdmin)



class SiteDiscountAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name',
        'scope_type', 'discount_type', 'value',
        'is_active', 'is_used', 'used_at', 'used_by',
        'start_date', 'end_date',
        'target_product',
    ]

    list_filter = [
        'scope_type', 'discount_type',
        'is_used', 'is_active', 'is_used'
    ]

    search_fields = [
        'code', 'name',
    ]


    #TODO : Return the store name target product belong

admin.site.register(SiteDiscount, SiteDiscountAdmin)


class DiscountUsageAdmin(admin.ModelAdmin):
    list_display = [
        "id", "discount_owner", "discount_code", "discount_type",
        "discount_value", "discount_amount", "used_by",
        "order", "order_item",
        "used_at", "created_at", "updated_at",
    ]

    list_filter = [
        "store_discount", "site_discount",
        "discount_type"
    ]

    search_fields = [
        "discount_code", "discount_type",
    ]

    def used_by(self,obj):
        return f"{obj.customer}"
admin.site.register(DiscountUsage, DiscountUsageAdmin)