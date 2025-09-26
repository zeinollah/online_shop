from django.contrib import admin
from .models import CustomerProfile



class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name",
        "phone_number","gender", "city","post_code","is_verified",
    ]
    list_filter = ["gender", "city", "is_verified",]
    search_fields = ["account__first_name", "account__last_name"]
    ordering = ['-created_at']

    def full_name(self,obj):
        return f"{obj.account.first_name} {obj.account.last_name}"
    full_name.short_description = "Name"

admin.site.register(CustomerProfile, CustomerProfileAdmin)