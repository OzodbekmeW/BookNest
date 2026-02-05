"""
Pydantic schemas for books, categories, authors
"""

from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class CategoryBase(BaseModel):
    """Base schema for category"""
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    """Schema for category response"""
    id: int
    slug: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    """Base schema for author"""
    name: str
    bio: Optional[str] = None
    nationality: Optional[str] = None


class AuthorResponse(AuthorBase):
    """Schema for author response"""
    id: int
    slug: str
    photo: Optional[str] = None
    birth_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PublisherResponse(BaseModel):
    """Schema for publisher response"""
    id: int
    name: str
    slug: str
    website: Optional[str] = None
    logo: Optional[str] = None
    
    class Config:
        from_attributes = True


class BookListItem(BaseModel):
    """Schema for book in list view"""
    id: int
    title: str
    slug: str
    author: str
    author_id: int
    category: str
    category_id: int
    price: Decimal
    discount_price: Optional[Decimal] = None
    final_price: Decimal
    discount_percentage: int
    cover_image: str
    rating: Decimal
    review_count: int
    is_in_stock: bool
    is_featured: bool
    is_bestseller: bool
    
    class Config:
        from_attributes = True


class BookDetail(BookListItem):
    """Schema for detailed book view"""
    subtitle: Optional[str] = None
    isbn: Optional[str] = None
    description: str
    publisher: str
    publisher_id: int
    stock: int
    pages: int
    language: str
    condition: str
    publication_year: int
    image_2: Optional[str] = None
    image_3: Optional[str] = None
    view_count: int
    created_at: datetime
    updated_at: datetime


class BookFilter(BaseModel):
    """Schema for book filtering"""
    category: Optional[List[int]] = None
    author: Optional[List[int]] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    language: Optional[List[str]] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    in_stock: Optional[bool] = None
    search: Optional[str] = None
    sort_by: Optional[str] = Field(None, regex='^(price|-price|rating|-rating|created|-created)$')
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
