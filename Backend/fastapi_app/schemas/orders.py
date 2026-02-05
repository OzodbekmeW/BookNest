"""
Pydantic schemas for orders
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from datetime import datetime


class OrderCreate(BaseModel):
    """Schema for creating order"""
    shipping_address_id: int
    payment_method: str = Field(..., regex='^(cash|card|paypal|stripe)$')
    coupon_code: Optional[str] = None
    notes: Optional[str] = None


class OrderItemResponse(BaseModel):
    """Schema for order item response"""
    id: int
    book_id: int
    book_title: str
    book_cover: str
    quantity: int
    price: Decimal
    subtotal: Decimal
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int
    order_number: str
    user_id: int
    items: List[OrderItemResponse]
    subtotal: Decimal
    shipping_cost: Decimal
    discount_amount: Decimal
    total: Decimal
    status: str
    payment_method: str
    is_paid: bool
    paid_at: Optional[datetime] = None
    tracking_number: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    delivered_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class OrderListItem(BaseModel):
    """Schema for order in list"""
    id: int
    order_number: str
    total: Decimal
    status: str
    is_paid: bool
    created_at: datetime
    items_count: int
    
    class Config:
        from_attributes = True


class CouponValidate(BaseModel):
    """Schema for coupon validation"""
    code: str
    subtotal: Decimal


class CouponResponse(BaseModel):
    """Schema for coupon response"""
    code: str
    discount_amount: Decimal
    message: str
