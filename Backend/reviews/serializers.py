"""
Serializers for Reviews app
"""
from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'title', 'comment', 
                  'is_verified_purchase', 'helpful_count', 'created_at', 'updated_at']
        read_only_fields = ['user', 'is_verified_purchase', 'helpful_count', 
                            'created_at', 'updated_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Baho 1 dan 5 gacha bo'lishi kerak")
        return value
