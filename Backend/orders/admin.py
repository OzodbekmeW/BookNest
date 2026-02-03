"""
Admin configuration for Orders app
"""

from django.contrib import admin
from .models import Coupon, Order, OrderItem


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Coupon admin"""
    
    list_display = [
        'code', 'discount_percentage', 'discount_amount',
        'min_purchase', 'used_count', 'max_uses',
        'valid_from', 'valid_to', 'is_active'
    ]
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Coupon Information', {
            'fields': ('code', 'is_active')
        }),
        ('Discount', {
            'fields': ('discount_percentage', 'discount_amount', 'min_purchase')
        }),
        ('Usage Limits', {
            'fields': ('max_uses', 'used_count')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_to')
        }),
    )


class OrderItemInline(admin.TabularInline):
    """Inline for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'quantity', 'price']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order admin with comprehensive features"""
    
    list_display = [
        'order_number', 'user', 'total', 'status',
        'payment_method', 'is_paid', 'created_at'
    ]
    list_filter = ['status', 'payment_method', 'is_paid', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'tracking_number']
    readonly_fields = [
        'order_number', 'created_at', 'updated_at',
        'subtotal', 'shipping_cost', 'discount_amount', 'total'
    ]
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'shipping_address')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'shipping_cost', 'discount_amount', 'total', 'coupon')
        }),
        ('Payment', {
            'fields': ('payment_method', 'is_paid', 'paid_at')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'tracking_number', 'delivered_at')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_confirmed', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected orders as confirmed"
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as shipped"
    
    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='delivered', delivered_at=timezone.now())
    mark_as_delivered.short_description = "Mark selected orders as delivered"

