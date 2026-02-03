"""
Serializers for Books app
"""
from rest_framework import serializers
from .models import Book, Category, Author, Publisher, Cart, CartItem, Wishlist


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    children = serializers.SerializerMethodField()
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'parent', 
                  'children', 'book_count', 'is_active', 'created_at']
        read_only_fields = ['slug', 'created_at']
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []
    
    def get_book_count(self, obj):
        return obj.book_set.count()


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author model"""
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'slug', 'bio', 'photo', 'birth_date', 
                  'nationality', 'book_count', 'created_at']
        read_only_fields = ['slug', 'created_at']
    
    def get_book_count(self, obj):
        return obj.book_set.count()


class PublisherSerializer(serializers.ModelSerializer):
    """Serializer for Publisher model"""
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'slug', 'website', 'logo', 'book_count', 'created_at']
        read_only_fields = ['slug', 'created_at']
    
    def get_book_count(self, obj):
        return obj.book_set.count()


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for book lists"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.name', read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'author_name', 'category_name', 
                  'publisher_name', 'price', 'original_price', 'discount_percentage',
                  'cover_image', 'average_rating', 'rating_count', 'stock', 
                  'is_featured', 'is_bestseller', 'language']
        read_only_fields = ['slug', 'average_rating', 'rating_count']
    
    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return round(((obj.original_price - obj.price) / obj.original_price) * 100)
        return 0
    
    def get_average_rating(self, obj):
        return obj.average_rating or 0


class BookDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single book view"""
    category = CategorySerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['slug', 'created_at', 'updated_at', 'average_rating', 'rating_count']
    
    def get_discount_percentage(self, obj):
        if obj.original_price and obj.original_price > obj.price:
            return round(((obj.original_price - obj.price) / obj.original_price) * 100)
        return 0
    
    def get_average_rating(self, obj):
        return obj.average_rating or 0


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    book = BookListSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity', 'subtotal', 'added_at']
        read_only_fields = ['subtotal', 'added_at']
    
    def get_subtotal(self, obj):
        return obj.book.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_items', 'total_price', 
                  'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())
    
    def get_total_price(self, obj):
        return sum(item.book.price * item.quantity for item in obj.items.all())


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for wishlist"""
    book = BookListSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'book', 'book_id', 'added_at']
        read_only_fields = ['added_at']
