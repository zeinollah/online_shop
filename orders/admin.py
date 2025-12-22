from itertools import count

from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "order_number", "order_status",
                    "shipping_phone", "shipping_city",
                    "shipping_address", "shipping_post_code",
                    "total_price", "payment_method", "is_paid","paid_at",
                    "created_at", "updated_at"]

    list_filter =["shipping_city", "order_status", "is_paid", "payment_method"]

    search_fields = ["shipping_city", ""]

    ordering =["-created_at"]

    readonly_fields = ['total_price']

admin.site.register(Order, OrderAdmin)




class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product_name",
                    "store_name", "quantity", "price", "subtotal", "discount"]

    # search_fields = ["order"]

    ordering = ["-created_at"]


admin.site.register(OrderItem, OrderItemAdmin)
