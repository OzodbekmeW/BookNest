"""
Views for Books app - API endpoints
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q, Avg, Count
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, Author, Publisher, Cart, CartItem, Wishlist
from .serializers import (
    BookListSerializer, BookDetailSerializer, CategorySerializer,
    AuthorSerializer, PublisherSerializer, CartSerializer, 
    CartItemSerializer, WishlistSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Category model"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet for Author model"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio', 'nationality']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class PublisherViewSet(viewsets.ModelViewSet):
    """ViewSet for Publisher model"""
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for Book model"""
    queryset = Book.objects.filter(is_active=True).select_related(
        'category', 'author', 'publisher'
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'publisher', 'language', 'is_featured', 'is_bestseller']
    search_fields = ['title', 'description', 'author__name', 'publisher__name']
    ordering_fields = ['title', 'price', 'created_at', 'average_rating', 'rating_count']
    ordering = ['-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.filter(average_rating__gte=min_rating)
        
        # Filter by stock availability
        in_stock = self.request.query_params.get('in_stock')
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured books"""
        books = self.get_queryset().filter(is_featured=True)[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def bestsellers(self, request):
        """Get bestseller books"""
        books = self.get_queryset().filter(is_bestseller=True).order_by('-rating_count')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new_arrivals(self, request):
        """Get new arrival books"""
        books = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    """ViewSet for Cart"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related('items__book')
    
    def get_object(self):
        """Get or create cart for current user"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Get current user's cart"""
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        cart = self.get_object()
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            book = Book.objects.get(id=book_id, is_active=True)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Kitob topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check stock
        if book.stock < quantity:
            return Response(
                {'error': 'Omborda yetarli miqdor yo\'q'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > book.stock:
                return Response(
                    {'error': 'Omborda yetarli miqdor yo\'q'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Update cart item quantity"""
        cart = self.get_object()
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))
        
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Mahsulot savatda topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if quantity <= 0:
            cart_item.delete()
        else:
            if quantity > cart_item.book.stock:
                return Response(
                    {'error': 'Omborda yetarli miqdor yo\'q'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = quantity
            cart_item.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Remove item from cart"""
        cart = self.get_object()
        item_id = request.data.get('item_id')
        
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Mahsulot savatda topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear all items from cart"""
        cart = self.get_object()
        cart.items.all().delete()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class WishlistViewSet(viewsets.ModelViewSet):
    """ViewSet for Wishlist"""
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('book')
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle book in wishlist"""
        book_id = request.data.get('book_id')
        
        try:
            book = Book.objects.get(id=book_id, is_active=True)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Kitob topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        wishlist_item = Wishlist.objects.filter(user=request.user, book=book).first()
        
        if wishlist_item:
            wishlist_item.delete()
            return Response(
                {'message': 'Sevimlilardan o\'chirildi', 'in_wishlist': False},
                status=status.HTTP_200_OK
            )
        else:
            Wishlist.objects.create(user=request.user, book=book)
            return Response(
                {'message': 'Sevimlilarga qo\'shildi', 'in_wishlist': True},
                status=status.HTTP_201_CREATED
            )


@api_view(['GET'])
def featured_books(request):
    """Get featured books"""
    books = Book.objects.filter(is_active=True, is_featured=True)[:10]
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def bestseller_books(request):
    """Get bestseller books"""
    books = Book.objects.filter(
        is_active=True, 
        is_bestseller=True
    ).order_by('-rating_count')[:10]
    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_books(request):
    """Search books by query"""
    query = request.GET.get('q', '')
    
    if not query:
        return Response({'error': 'Qidiruv so\'zi kiritilmagan'}, status=status.HTTP_400_BAD_REQUEST)
    
    books = Book.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(author__name__icontains=query) |
        Q(publisher__name__icontains=query)
    ).filter(is_active=True).distinct()
    
    serializer = BookListSerializer(books, many=True)
    return Response({
        'query': query,
        'count': books.count(),
        'results': serializer.data
    })
