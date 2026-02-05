"""
Dependencies for FastAPI routes
Authentication and authorization utilities
"""

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from decouple import config
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from users.models import User

security = HTTPBearer()

SECRET_KEY = config('JWT_SECRET_KEY', default=config('SECRET_KEY'))
ALGORITHM = config('JWT_ALGORITHM', default='HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)


def create_access_token(data: dict):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    """Get current authenticated user from token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found")


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_optional_user(credentials: HTTPAuthorizationCredentials = Security(security, auto_error=False)):
    """Get user if authenticated, None otherwise (for optional auth)"""
    if credentials is None:
        return None
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        return None
    
    user_id = payload.get("user_id")
    if user_id is None:
        return None
    
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None
