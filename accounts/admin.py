from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'birth_day' ,'user_roll',
                    'email', 'phone_number', 'city', 'address', 'post_code', 'is_staff','is_active']
    list_filter = ['user_roll', 'city']
    search_fields = ['email', 'last_name', 'phone_number', 'address']
    ordering = ["-created_at"]
admin.site.register(User, UserAdmin)