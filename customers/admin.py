from django.contrib import admin
from .models import CustomerProfile



class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email",
        "phone_number","gender", "city","post_code", "is_active", "is_verified",
    ]
    list_filter = ["gender", "city", "is_verified",]
    search_fields = ["account__first_name", "account__last_name", "account__email"]
    ordering = ['-created_at']

    def email(self, obj):
        return obj.account.email
    email.admin_order_field = 'account'

    def is_active(self,obj):
        return obj.account.is_active
    is_active.boolean = True
    is_active.admin_order_field = 'is_active'

    def full_name(self,obj):
        return f"{obj.account.first_name} {obj.account.last_name}"
    full_name.short_description = "Name"

admin.site.register(CustomerProfile, CustomerProfileAdmin)