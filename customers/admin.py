from django.contrib import admin
from .models import CustomerProfile, Wallet, Transaction



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


class WalletAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "balance", "created_at", "updated_at"]
    search_fields = ["customer__account__first_name", "customer__account__last_name"]

    def customer_name(self, obj):
        return obj.customer.full_name.capitalize()

admin.site.register(Wallet, WalletAdmin)



class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id", "wallet", "transaction_type", "order",
        "amount", "created_at",
    ]

    list_filter = ["wallet", "transaction_type",]

    search_fields = ["customer_name"]

    def customer_name(self, obj):
        return obj.customer.full_name

admin.site.register(Transaction, TransactionAdmin)