"""
Pydantic schemas for authentication and user management
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, date


class UserRegister(BaseModel):
    """Schema for user registration"""
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    
    @validator('password_confirm')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    """Schema for user profile"""
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    avatar: Optional[str]
    date_of_birth: Optional[date]
    is_email_verified: bool
    date_joined: datetime
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None


class ChangePassword(BaseModel):
    """Schema for changing password"""
    old_password: str
    new_password: str = Field(..., min_length=8)
    new_password_confirm: str
    
    @validator('new_password_confirm')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v


class AddressCreate(BaseModel):
    """Schema for creating address"""
    full_name: str
    phone: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "Uzbekistan"
    is_default: bool = False


class AddressResponse(AddressCreate):
    """Schema for address response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
