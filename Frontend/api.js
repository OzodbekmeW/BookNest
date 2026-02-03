// ==========================================
// BOOKNEST - API INTEGRATION
// ==========================================

// API Configuration
const API_CONFIG = {
  baseURL: 'http://127.0.0.1:8000/api',
  endpoints: {
    books: '/books/books/',
    categories: '/books/categories/',
    authors: '/books/authors/',
    cart: '/books/cart/',
    wishlist: '/books/wishlist/',
    orders: '/orders/',
    reviews: '/reviews/',
    auth: '/auth/'
  },
  timeout: 10000
};

// API Client Class
class APIClient {
  constructor(config) {
    this.baseURL = config.baseURL;
    this.endpoints = config.endpoints;
    this.timeout = config.timeout;
  }
  
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };
    
    try {
      const response = await fetch(url, defaultOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      console.error('API Request Error:', error);
      return { success: false, error: error.message };
    }
  }
  
  // Books API
  async getBooks(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = `${this.endpoints.books}${queryString ? `?${queryString}` : ''}`;
    return await this.request(endpoint);
  }
  
  async getBook(slug) {
    return await this.request(`${this.endpoints.books}${slug}/`);
  }
  
  async searchBooks(query) {
    return await this.request(`${this.endpoints.books}?search=${encodeURIComponent(query)}`);
  }
  
  async getFeaturedBooks() {
    return await this.request(`${this.endpoints.books}?is_featured=true`);
  }
  
  async getBestsellers() {
    return await this.request(`${this.endpoints.books}?is_bestseller=true`);
  }
  
  // Categories API
  async getCategories() {
    return await this.request(this.endpoints.categories);
  }
  
  async getCategory(slug) {
    return await this.request(`${this.endpoints.categories}${slug}/`);
  }
  
  // Cart API
  async getCart() {
    return await this.request(`${this.endpoints.cart}my_cart/`);
  }
  
  async addToCart(bookId, quantity = 1) {
    return await this.request(`${this.endpoints.cart}add_item/`, {
      method: 'POST',
      body: JSON.stringify({ book_id: bookId, quantity })
    });
  }
  
  async updateCartItem(itemId, quantity) {
    return await this.request(`${this.endpoints.cart}update_item/`, {
      method: 'POST',
      body: JSON.stringify({ item_id: itemId, quantity })
    });
  }
  
  async removeFromCart(itemId) {
    return await this.request(`${this.endpoints.cart}remove_item/`, {
      method: 'POST',
      body: JSON.stringify({ item_id: itemId })
    });
  }
  
  // Wishlist API
  async getWishlist() {
    return await this.request(this.endpoints.wishlist);
  }
  
  async toggleWishlist(bookId) {
    return await this.request(`${this.endpoints.wishlist}toggle/`, {
      method: 'POST',
      body: JSON.stringify({ book_id: bookId })
    });
  }
  
  // Orders API
  async createOrder(orderData) {
    return await this.request(`${this.endpoints.orders}create_from_cart/`, {
      method: 'POST',
      body: JSON.stringify(orderData)
    });
  }
  
  async getOrders() {
    return await this.request(this.endpoints.orders);
  }
  
  async getOrder(orderId) {
    return await this.request(`${this.endpoints.orders}${orderId}/`);
  }
}

// Create global API client instance
const api = new APIClient(API_CONFIG);

// Export for use in other scripts
window.api = api;
window.API_CONFIG = API_CONFIG;

console.log('API Client initialized:', API_CONFIG.baseURL);
