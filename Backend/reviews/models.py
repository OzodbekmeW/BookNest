"""
Reviews models for BookNest E-commerce Platform
Models for book reviews and ratings
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from books.models import Book


class Review(models.Model):
    """Book reviews and ratings"""
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars'
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(
        default=False,
        help_text='Whether the user purchased this book'
    )
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ['user', 'book']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['book', '-created_at']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}★)"
    
    def save(self, *args, **kwargs):
        """Update book rating when review is saved"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        self.update_book_rating()
    
    def delete(self, *args, **kwargs):
        """Update book rating when review is deleted"""
        super().delete(*args, **kwargs)
        self.update_book_rating()
    
    def update_book_rating(self):
        """Recalculate book's average rating and review count"""
        reviews = Review.objects.filter(book=self.book)
        count = reviews.count()
        
        if count > 0:
            avg_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.book.rating = round(avg_rating, 2)
            self.book.review_count = count
        else:
            self.book.rating = 0
            self.book.review_count = 0
        
        self.book.save()

