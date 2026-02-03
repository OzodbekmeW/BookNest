"""
Admin configuration for Reviews app
"""

from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review admin"""
    
    list_display = [
        'user', 'book', 'rating', 'title',
        'is_verified_purchase', 'helpful_count', 'created_at'
    ]
    list_filter = ['rating', 'is_verified_purchase', 'created_at']
    search_fields = ['user__username', 'book__title', 'title', 'comment']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'book', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_verified_purchase', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

