"""
Pydantic schemas for reviews
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReviewCreate(BaseModel):
    """Schema for creating review"""
    book_id: int
    rating: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=5, max_length=200)
    comment: str = Field(..., min_length=10)


class ReviewUpdate(BaseModel):
    """Schema for updating review"""
    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    comment: Optional[str] = Field(None, min_length=10)


class ReviewResponse(BaseModel):
    """Schema for review response"""
    id: int
    user_id: int
    user_name: str
    user_avatar: Optional[str] = None
    book_id: int
    rating: int
    title: str
    comment: str
    is_verified_purchase: bool
    helpful_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
