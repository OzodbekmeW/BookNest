"""
Books routes for FastAPI
Browse, search, filter books
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from django.db.models import Q
from django.core.paginator import Paginator

from books.models import Book, Category, Author
from ..schemas.books import BookListItem, BookDetail, CategoryResponse, AuthorResponse
from ..dependencies import get_optional_user

router = APIRouter(prefix="/api/books", tags=["Books"])


@router.get("/", response_model=dict)
async def get_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[List[int]] = Query(None),
    author: Optional[List[int]] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    language: Optional[List[str]] = Query(None),
    rating: Optional[int] = Query(None, ge=1, le=5),
    in_stock: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("-created_at"),
    user = Depends(get_optional_user)
):
    """Get all books with filters and pagination"""
    queryset = Book.objects.filter(is_active=True).select_related('author', 'category', 'publisher')
    
    # Apply filters
    if category:
        queryset = queryset.filter(category_id__in=category)
    if author:
        queryset = queryset.filter(author_id__in=author)
    if min_price is not None:
        queryset = queryset.filter(price__gte=min_price)
    if max_price is not None:
        queryset = queryset.filter(price__lte=max_price)
    if language:
        queryset = queryset.filter(language__in=language)
    if rating:
        queryset = queryset.filter(rating__gte=rating)
    if in_stock:
        queryset = queryset.filter(stock__gt=0)
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(subtitle__icontains=search) |
            Q(description__icontains=search) |
            Q(author__name__icontains=search) |
            Q(isbn__icontains=search)
        )
    
    # Sorting
    queryset = queryset.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)
    
    books = [
        {
            "id": book.id,
            "title": book.title,
            "slug": book.slug,
            "author": book.author.name,
            "author_id": book.author.id,
            "category": book.category.name,
            "category_id": book.category.id,
            "price": float(book.price),
            "discount_price": float(book.discount_price) if book.discount_price else None,
            "final_price": float(book.final_price),
            "discount_percentage": book.discount_percentage,
            "cover_image": str(book.cover_image) if book.cover_image else "",
            "rating": float(book.rating),
            "review_count": book.review_count,
            "is_in_stock": book.is_in_stock,
            "is_featured": book.is_featured,
            "is_bestseller": book.is_bestseller,
        }
        for book in page_obj
    ]
    
    return {
        "books": books,
        "total": paginator.count,
        "page": page,
        "page_size": page_size,
        "total_pages": paginator.num_pages
    }


@router.get("/featured", response_model=List[BookListItem])
async def get_featured_books(limit: int = Query(10, ge=1, le=50)):
    """Get featured books"""
    books = Book.objects.filter(is_active=True, is_featured=True).select_related('author', 'category')[:limit]
    return [
        {
            "id": book.id,
            "title": book.title,
            "slug": book.slug,
            "author": book.author.name,
            "author_id": book.author.id,
            "category": book.category.name,
            "category_id": book.category.id,
            "price": float(book.price),
            "discount_price": float(book.discount_price) if book.discount_price else None,
            "final_price": float(book.final_price),
            "discount_percentage": book.discount_percentage,
            "cover_image": str(book.cover_image),
            "rating": float(book.rating),
            "review_count": book.review_count,
            "is_in_stock": book.is_in_stock,
            "is_featured": book.is_featured,
            "is_bestseller": book.is_bestseller,
        }
        for book in books
    ]


@router.get("/bestsellers", response_model=List[BookListItem])
async def get_bestsellers(limit: int = Query(10, ge=1, le=50)):
    """Get bestseller books"""
    books = Book.objects.filter(is_active=True, is_bestseller=True).select_related('author', 'category')[:limit]
    return [
        {
            "id": book.id,
            "title": book.title,
            "slug": book.slug,
            "author": book.author.name,
            "author_id": book.author.id,
            "category": book.category.name,
            "category_id": book.category.id,
            "price": float(book.price),
            "discount_price": float(book.discount_price) if book.discount_price else None,
            "final_price": float(book.final_price),
            "discount_percentage": book.discount_percentage,
            "cover_image": str(book.cover_image),
            "rating": float(book.rating),
            "review_count": book.review_count,
            "is_in_stock": book.is_in_stock,
            "is_featured": book.is_featured,
            "is_bestseller": book.is_bestseller,
        }
        for book in books
    ]


@router.get("/new-arrivals", response_model=List[BookListItem])
async def get_new_arrivals(limit: int = Query(10, ge=1, le=50)):
    """Get newly added books"""
    books = Book.objects.filter(is_active=True).select_related('author', 'category').order_by('-created_at')[:limit]
    return [
        {
            "id": book.id,
            "title": book.title,
            "slug": book.slug,
            "author": book.author.name,
            "author_id": book.author.id,
            "category": book.category.name,
            "category_id": book.category.id,
            "price": float(book.price),
            "discount_price": float(book.discount_price) if book.discount_price else None,
            "final_price": float(book.final_price),
            "discount_percentage": book.discount_percentage,
            "cover_image": str(book.cover_image),
            "rating": float(book.rating),
            "review_count": book.review_count,
            "is_in_stock": book.is_in_stock,
            "is_featured": book.is_featured,
            "is_bestseller": book.is_bestseller,
        }
        for book in books
    ]


@router.get("/{book_id}", response_model=BookDetail)
async def get_book_detail(book_id: int):
    """Get book detail and increment view count"""
    try:
        book = Book.objects.select_related('author', 'category', 'publisher').get(id=book_id, is_active=True)
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Increment view count
    book.view_count += 1
    book.save(update_fields=['view_count'])
    
    return {
        "id": book.id,
        "title": book.title,
        "slug": book.slug,
        "subtitle": book.subtitle,
        "isbn": book.isbn,
        "description": book.description,
        "author": book.author.name,
        "author_id": book.author.id,
        "category": book.category.name,
        "category_id": book.category.id,
        "publisher": book.publisher.name,
        "publisher_id": book.publisher.id,
        "price": float(book.price),
        "discount_price": float(book.discount_price) if book.discount_price else None,
        "final_price": float(book.final_price),
        "discount_percentage": book.discount_percentage,
        "stock": book.stock,
        "pages": book.pages,
        "language": book.language,
        "condition": book.condition,
        "publication_year": book.publication_year,
        "cover_image": str(book.cover_image),
        "image_2": str(book.image_2) if book.image_2 else None,
        "image_3": str(book.image_3) if book.image_3 else None,
        "rating": float(book.rating),
        "review_count": book.review_count,
        "view_count": book.view_count,
        "is_in_stock": book.is_in_stock,
        "is_featured": book.is_featured,
        "is_bestseller": book.is_bestseller,
        "created_at": book.created_at,
        "updated_at": book.updated_at,
    }


@router.get("/related/{book_id}", response_model=List[BookListItem])
async def get_related_books(book_id: int, limit: int = Query(6, ge=1, le=20)):
    """Get related books by category and author"""
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Get books from same category or by same author
    related = Book.objects.filter(
        Q(category=book.category) | Q(author=book.author),
        is_active=True
    ).exclude(id=book_id).select_related('author', 'category').distinct()[:limit]
    
    return [
        {
            "id": b.id,
            "title": b.title,
            "slug": b.slug,
            "author": b.author.name,
            "author_id": b.author.id,
            "category": b.category.name,
            "category_id": b.category.id,
            "price": float(b.price),
            "discount_price": float(b.discount_price) if b.discount_price else None,
            "final_price": float(b.final_price),
            "discount_percentage": b.discount_percentage,
            "cover_image": str(b.cover_image),
            "rating": float(b.rating),
            "review_count": b.review_count,
            "is_in_stock": b.is_in_stock,
            "is_featured": b.is_featured,
            "is_bestseller": b.is_bestseller,
        }
        for b in related
    ]
