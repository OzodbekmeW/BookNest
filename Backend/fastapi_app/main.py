"""
FastAPI Main Application
BookNest E-commerce Platform API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from decouple import config
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

# Import routers
from .routes import auth, books

# Create FastAPI app
app = FastAPI(
    title="BookNest API",
    description="E-commerce API for BookNest book store",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config('CORS_ALLOWED_ORIGINS', default='*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(books.router)

# Mount media files
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'
if MEDIA_ROOT.exists():
    app.mount("/media", StaticFiles(directory=str(MEDIA_ROOT)), name="media")


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to BookNest API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config('FASTAPI_HOST', default='0.0.0.0'),
        port=config('FASTAPI_PORT', default=8001, cast=int),
        reload=True
    )
