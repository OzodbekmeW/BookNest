"""
Pydantic schemas for cart and wishlist
"""

from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal
from datetime import datetime


class CartItemAdd(BaseModel):
    """Schema for adding item to cart"""
    book_id: int
    quantity: int = Field(1, ge=1)


class CartItemUpdate(BaseModel):
    """Schema for updating cart item"""
    quantity: int = Field(..., ge=1)


class CartItemResponse(BaseModel):
    """Schema for cart item response"""
    id: int
    book_id: int
    book_title: str
    book_cover: str
    book_price: Decimal
    book_discount_price: Optional[Decimal] = None
    quantity: int
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Schema for cart response"""
    id: int
    items: List[CartItemResponse]
    total_items: int
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class WishlistAdd(BaseModel):
    """Schema for adding to wishlist"""
    book_id: int


class WishlistResponse(BaseModel):
    """Schema for wishlist response"""
    id: int
    book_id: int
    book_title: str
    book_cover: str
    book_price: Decimal
    book_discount_price: Optional[Decimal] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
