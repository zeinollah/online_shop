from django.contrib import admin
from .models import SellerDiscount, SiteDiscount


class SellerDiscountAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name', 'store_name',
        'scope_type', 'discount_type', 'value',
        'is_active', 'is_used', 'used_at', 'used_by',
        'start_date', 'end_date',
        'target_product', 'target_product'
    ]

    list_filter = [
        'seller',
        'scope_type', 'discount_type',
        'is_used', 'is_active', 'is_used'
    ]

    search_fields = [
        'code', 'name', 'seller__store_name',
        'seller__seller__name',
    ]

    def store_name(self,obj):
        return f"{obj.seller.store_name}"
    store_name.admin_order_field = 'Store_Name'

admin.site.register(SellerDiscount, SellerDiscountAdmin)




class SiteDiscountAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'name',
        'scope_type', 'discount_type', 'value',
        'is_active', 'is_used', 'used_at', 'used_by',
        'start_date', 'end_date',
        'target_product', 'target_product'
    ]

    list_filter = [
        'scope_type', 'discount_type',
        'is_used', 'is_active', 'is_used'
    ]

    search_fields = [
        'code', 'name',
    ]

admin.site.register(SiteDiscount, SiteDiscountAdmin)