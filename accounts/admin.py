from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name' ,'user_roll']
    list_filter = ['user_roll', 'is_active','is_staff']
    search_fields = ['email', 'last_name']
    fieldsets = (
        (None,
         {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates',
         {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields',
         {'fields': ('user_roll',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'user_roll'),
        }),
    )

    ordering = ["-created_at"]
admin.site.register(User, UserAdmin)