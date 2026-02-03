"""
Views for Reviews app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer
from books.models import Book
from orders.models import Order


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review model"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'book')
        book_id = self.request.query_params.get('book')
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        return queryset
    
    def perform_create(self, serializer):
        # Check if user purchased the book
        book = serializer.validated_data['book']
        user = self.request.user
        
        has_purchased = Order.objects.filter(
            user=user,
            items__book=book,
            status__in=['delivered', 'completed']
        ).exists()
        
        serializer.save(
            user=user,
            is_verified_purchase=has_purchased
        )
    
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        """Mark review as helpful"""
        review = self.get_object()
        review.helpful_count += 1
        review.save()
        
        serializer = self.get_serializer(review)
        return Response(serializer.data)
