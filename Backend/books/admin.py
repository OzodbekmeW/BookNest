"""
Admin configuration for Books app
"""

from django.contrib import admin
from .models import Category, Author, Publisher, Book, Cart, CartItem, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin"""
    
    list_display = ['name', 'slug', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Author admin"""
    
    list_display = ['name', 'slug', 'nationality', 'birth_date', 'created_at']
    list_filter = ['nationality']
    search_fields = ['name', 'bio', 'nationality']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Publisher admin"""
    
    list_display = ['name', 'slug', 'website', 'created_at']
    search_fields = ['name', 'website']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book admin with advanced features"""
    
    list_display = [
        'title', 'author', 'category', 'price', 'discount_price',
        'stock', 'rating', 'is_featured', 'is_bestseller', 'is_active', 'created_at'
    ]
    list_filter = [
        'is_active', 'is_featured', 'is_bestseller', 'category',
        'author', 'language', 'condition', 'created_at'
    ]
    search_fields = ['title', 'subtitle', 'isbn', 'description', 'author__name']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    readonly_fields = ['rating', 'review_count', 'view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'subtitle', 'isbn', 'description')
        }),
        ('Relationships', {
            'fields': ('author', 'category', 'publisher')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'discount_price', 'stock')
        }),
        ('Book Details', {
            'fields': ('pages', 'language', 'condition', 'publication_year')
        }),
        ('Images', {
            'fields': ('cover_image', 'image_2', 'image_3')
        }),
        ('Metrics', {
            'fields': ('rating', 'review_count', 'view_count')
        }),
        ('Flags', {
            'fields': ('is_featured', 'is_bestseller', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_bestseller', 'mark_as_active', 'mark_as_inactive']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected books as featured"
    
    def mark_as_bestseller(self, request, queryset):
        queryset.update(is_bestseller=True)
    mark_as_bestseller.short_description = "Mark selected books as bestseller"
    
    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_as_active.short_description = "Mark selected books as active"
    
    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_as_inactive.short_description = "Mark selected books as inactive"


class CartItemInline(admin.TabularInline):
    """Inline for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart admin"""
    
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]
    ordering = ['-updated_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Wishlist admin"""
    
    list_display = ['user', 'book', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title']
    ordering = ['-created_at']

