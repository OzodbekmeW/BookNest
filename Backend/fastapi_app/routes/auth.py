"""
Authentication routes for FastAPI
Login, register, profile management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

from ..schemas.auth import (
    UserRegister, UserLogin, TokenResponse, UserProfile,
    UserProfileUpdate, ChangePassword, AddressCreate, AddressResponse
)
from ..dependencies import create_access_token, create_refresh_token, get_current_active_user
from users.models import User, Address

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """Register a new user"""
    try:
        # Create new user
        user = User.objects.create(
            username=user_data.username,
            email=user_data.email,
            password=make_password(user_data.password),
            first_name=user_data.first_name or "",
            last_name=user_data.last_name or "",
            phone=user_data.phone or ""
        )
        
        # Generate tokens
        access_token = create_access_token({"user_id": user.id})
        refresh_token = create_refresh_token({"user_id": user.id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
        
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """Login user and return JWT tokens"""
    try:
        # Find user by username or email
        user = User.objects.get(username=credentials.username)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=credentials.username)
        except User.DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    
    # Verify password
    if not check_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is disabled"
        )
    
    # Generate tokens
    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone": current_user.phone,
        "avatar": str(current_user.avatar) if current_user.avatar else None,
        "date_of_birth": current_user.date_of_birth,
        "is_email_verified": current_user.is_email_verified,
        "date_joined": current_user.date_joined
    }


@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update user profile"""
    if profile_data.first_name is not None:
        current_user.first_name = profile_data.first_name
    if profile_data.last_name is not None:
        current_user.last_name = profile_data.last_name
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    if profile_data.date_of_birth is not None:
        current_user.date_of_birth = profile_data.date_of_birth
    
    current_user.save()
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone": current_user.phone,
        "avatar": str(current_user.avatar) if current_user.avatar else None,
        "date_of_birth": current_user.date_of_birth,
        "is_email_verified": current_user.is_email_verified,
        "date_joined": current_user.date_joined
    }


@router.post("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user)
):
    """Change user password"""
    # Verify old password
    if not check_password(password_data.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password = make_password(password_data.new_password)
    current_user.save()
    
    return {"message": "Password changed successfully"}


@router.post("/addresses", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(
    address_data: AddressCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create new address"""
    address = Address.objects.create(
        user=current_user,
        **address_data.dict()
    )
    return address


@router.get("/addresses", response_model=list[AddressResponse])
async def get_addresses(current_user: User = Depends(get_current_active_user)):
    """Get all user addresses"""
    addresses = Address.objects.filter(user=current_user)
    return list(addresses)


@router.put("/addresses/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    address_data: AddressCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Update address"""
    try:
        address = Address.objects.get(id=address_id, user=current_user)
    except Address.DoesNotExist:
        raise HTTPException(status_code=404, detail="Address not found")
    
    for field, value in address_data.dict().items():
        setattr(address, field, value)
    address.save()
    
    return address


@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Delete address"""
    try:
        address = Address.objects.get(id=address_id, user=current_user)
        address.delete()
    except Address.DoesNotExist:
        raise HTTPException(status_code=404, detail="Address not found")


@router.put("/addresses/{address_id}/set-default", response_model=AddressResponse)
async def set_default_address(
    address_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """Set address as default"""
    try:
        address = Address.objects.get(id=address_id, user=current_user)
        address.is_default = True
        address.save()
        return address
    except Address.DoesNotExist:
        raise HTTPException(status_code=404, detail="Address not found")
