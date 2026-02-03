"""
Serializers for Orders app
"""
from rest_framework import serializers
from .models import Order, OrderItem
from books.serializers import BookListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    book = BookListSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'quantity', 'price', 'subtotal']
        read_only_fields = ['price']
    
    def get_subtotal(self, obj):
        return obj.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders"""
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'items', 'total_amount', 
                  'total_items', 'status', 'payment_method', 'payment_status',
                  'shipping_address', 'shipping_city', 'shipping_postal_code',
                  'phone', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['order_number', 'user', 'created_at', 'updated_at']
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
