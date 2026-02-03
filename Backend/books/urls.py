from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'publishers', views.PublisherViewSet, basename='publisher')
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'wishlist', views.WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
    path('featured/', views.featured_books, name='featured-books'),
    path('bestsellers/', views.bestseller_books, name='bestseller-books'),
    path('search/', views.search_books, name='search-books'),
]
