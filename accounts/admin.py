from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'user_roll', 'email', 'phone_number', 'city', 'address']
    list_filter = ['user_roll', 'city']
    search_fields = ['email','last_name','phone_number','address']
    ordering = ["-created_at"]
admin.site.register(User, UserAdmin)