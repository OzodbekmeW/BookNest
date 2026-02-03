"""
Views for Orders app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderSerializer
from books.models import Book, Cart


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for Order model"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__book')
    
    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        """Create order from cart"""
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Savat bo\'sh'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not cart.items.exists():
            return Response(
                {'error': 'Savatda mahsulot yo\'q'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required fields
        required_fields = ['shipping_address', 'shipping_city', 'phone']
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {'error': f'{field} maydoni to\'ldirilishi shart'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create order
        with transaction.atomic():
            # Calculate total
            total_amount = sum(
                item.book.price * item.quantity 
                for item in cart.items.select_related('book')
            )
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                shipping_address=request.data.get('shipping_address'),
                shipping_city=request.data.get('shipping_city'),
                shipping_postal_code=request.data.get('shipping_postal_code', ''),
                phone=request.data.get('phone'),
                notes=request.data.get('notes', ''),
                payment_method=request.data.get('payment_method', 'cash_on_delivery')
            )
            
            # Create order items from cart
            for cart_item in cart.items.select_related('book'):
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    price=cart_item.book.price
                )
                
                # Update book stock
                book = cart_item.book
                book.stock -= cart_item.quantity
                book.save()
            
            # Clear cart
            cart.items.all().delete()
            
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel order"""
        order = self.get_object()
        
        if order.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Bu buyurtmani bekor qilib bo\'lmaydi'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Return stock
            for item in order.items.select_related('book'):
                book = item.book
                book.stock += item.quantity
                book.save()
            
            order.status = 'cancelled'
            order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)
