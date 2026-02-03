"""
Admin configuration for Users app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_email_verified', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'is_email_verified', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone', 'avatar', 'date_of_birth', 'is_email_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone', 'avatar', 'date_of_birth')
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Address admin"""
    
    list_display = ['user', 'full_name', 'city', 'country', 'is_default', 'created_at']
    list_filter = ['is_default', 'country', 'city']
    search_fields = ['user__username', 'full_name', 'phone', 'city', 'postal_code']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('full_name', 'phone')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Settings', {
            'fields': ('is_default',)
        }),
    )

