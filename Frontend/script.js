// ==========================================
// BOOKNEST - INTERACTIVE FUNCTIONALITY
// ==========================================

// ==========================================
// GLOBAL VARIABLES
// ==========================================
let cart = [];
let favorites = [];
let currentBooks = [];
let filteredBooks = [];

// Sample book data
const sampleBooks = [
  {
    id: 1,
    title: "O'tgan kunlar",
    author: "Abdulla Qodiriy",
    category: "klassik",
    price: 45000,
    originalPrice: 60000,
    rating: 4.8,
    ratingCount: 256,
    cover: "bg-gradient-1",
    icon: "📚",
    description: "O'zbek adabiyotining bepul klassikasi"
  },
  {
    id: 2,
    title: "Alpomish",
    author: "Xalq og'zaki ijodi",
    category: "dostoner",
    price: 38000,
    originalPrice: 50000,
    rating: 4.9,
    ratingCount: 189,
    cover: "bg-gradient-2",
    icon: "⚔️",
    description: "O'zbek xalqining buyuk dostoni"
  },
  {
    id: 3,
    title: "Xamsa",
    author: "Alisher Navoiy",
    category: "sherlar",
    price: 75000,
    originalPrice: 95000,
    rating: 4.9,
    ratingCount: 342,
    cover: "bg-gradient-3",
    icon: "🎭",
    description: "Buyuk shoirning ulug' asari"
  },
  {
    id: 4,
    title: "Yer yuzidagi eng chiroyli yer",
    author: "Murod Muhammad Do'st",
    category: "zamonaviy",
    price: 42000,
    originalPrice: 55000,
    rating: 4.7,
    ratingCount: 156,
    cover: "bg-gradient-1",
    icon: "🌍",
    description: "Zamonaviy o'zbek adabiyotidan ajoyib asar"
  },
  {
    id: 5,
    title: "Baxtli kunlar",
    author: "Said Ahmad",
    category: "yoshlar",
    price: 35000,
    originalPrice: 45000,
    rating: 4.6,
    ratingCount: 89,
    cover: "bg-gradient-2",
    icon: "🌟",
    description: "Yoshlar uchun mo'ljallangan qiziqarli roman"
  },
  {
    id: 6,
    title: "Dizayn asoslari",
    author: "Jamoliddin Karimov",
    category: "texnik",
    price: 68000,
    originalPrice: 85000,
    rating: 4.5,
    ratingCount: 234,
    cover: "bg-gradient-3",
    icon: "💻",
    description: "Dizayn va texnologiya haqida"
  }
];

// ==========================================
// UTILITY FUNCTIONS
// ==========================================
function formatPrice(price) {
  return price.toLocaleString('uz-UZ') + " so'm";
}

function generateStars(rating) {
  const fullStars = Math.floor(rating);
  const hasHalfStar = rating % 1 !== 0;
  let stars = '';
  
  for (let i = 0; i < fullStars; i++) {
    stars += '★';
  }
  
  if (hasHalfStar) {
    stars += '☆';
  }
  
  while (stars.length < 5) {
    stars += '☆';
  }
  
  return stars;
}

function calculateDiscount(original, current) {
  return Math.round(((original - current) / original) * 100);
}

function showNotification(message, type = 'success') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
    <span>${message}</span>
  `;
  
  // Add notification styles
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'success' ? '#10b981' : '#ef4444'};
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    z-index: 10000;
    transform: translateX(400px);
    transition: transform 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  `;
  
  document.body.appendChild(notification);
  
  // Animate in
  setTimeout(() => {
    notification.style.transform = 'translateX(0)';
  }, 100);
  
  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.transform = 'translateX(400px)';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 3000);
}

// ==========================================
// NAVIGATION
// ==========================================
class Navigation {
  constructor() {
    this.navbar = document.querySelector('.navbar');
    this.mobileToggle = document.querySelector('.mobile-toggle');
    this.navMenu = document.querySelector('.nav-menu');
    this.searchInput = document.querySelector('.search-input');
    this.searchBtn = document.querySelector('.search-btn');
    this.cartBtn = document.querySelector('.cart-btn');
    this.cartBadge = document.querySelector('.cart-badge');
    this.wishlistBtn = document.querySelector('.wishlist-btn');
    this.wishlistBadge = document.querySelector('.wishlist-badge');
    
    this.init();
  }
  
  init() {
    this.handleScroll();
    this.handleMobileMenu();
    this.handleSearch();
    this.updateBadges();
  }
  
  handleScroll() {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 100) {
        this.navbar.classList.add('scrolled');
      } else {
        this.navbar.classList.remove('scrolled');
      }
    });
  }
  
  handleMobileMenu() {
    if (this.mobileToggle) {
      this.mobileToggle.addEventListener('click', () => {
        this.navMenu.classList.toggle('active');
        this.mobileToggle.classList.toggle('active');
      });
    }
  }
  
  handleSearch() {
    if (this.searchBtn) {
      this.searchBtn.addEventListener('click', () => {
        this.performSearch();
      });
    }
    
    if (this.searchInput) {
      this.searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.performSearch();
        }
      });
    }
  }
  
  performSearch() {
    const query = this.searchInput.value.trim().toLowerCase();
    if (query) {
      const results = sampleBooks.filter(book => 
        book.title.toLowerCase().includes(query) ||
        book.author.toLowerCase().includes(query) ||
        book.category.toLowerCase().includes(query)
      );
      
      this.displaySearchResults(results, query);
      showNotification(`${results.length} ta kitob topildi: "${query}"`);
    }
  }
  
  displaySearchResults(results, query) {
    // Scroll to books section
    document.querySelector('.featured-books').scrollIntoView({
      behavior: 'smooth'
    });
    
    // Update books display
    setTimeout(() => {
      bookManager.displayBooks(results);
      
      // Update section title
      const sectionTitle = document.querySelector('.featured-books .section-title');
      sectionTitle.textContent = `"${query}" bo'yicha qidiruv natijalari`;
    }, 500);
  }
  
  updateBadges() {
    if (this.cartBadge) {
      this.cartBadge.textContent = cart.length;
      this.cartBadge.style.display = cart.length > 0 ? 'block' : 'none';
    }
    
    if (this.wishlistBadge) {
      this.wishlistBadge.textContent = favorites.length;
      this.wishlistBadge.style.display = favorites.length > 0 ? 'block' : 'none';
    }
  }
}

// ==========================================
// BOOK MANAGEMENT
// ==========================================
class BookManager {
  constructor() {
    this.booksContainer = document.querySelector('.books-grid');
    this.filterTabs = document.querySelectorAll('.filter-tab');
    this.loadMoreBtn = document.querySelector('.load-more-btn');
    this.apiBaseUrl = 'http://127.0.0.1:8000';
    
    this.init();
  }
  
  async init() {
    await this.loadBooksFromAPI();
    this.setupFilters();
    this.displayBooks(filteredBooks);
    this.setupLoadMore();
  }
  
  async loadBooksFromAPI() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/books/books/`);
      if (response.ok) {
        const data = await response.json();
        const apiBooks = data.results.map(book => ({
          id: book.id,
          title: book.title,
          author: book.author.name,
          category: book.category.slug,
          price: parseFloat(book.price),
          originalPrice: book.discount_price ? parseFloat(book.discount_price) : parseFloat(book.price) * 1.2,
          rating: parseFloat(book.rating),
          ratingCount: book.review_count,
          cover: 'book-cover',
          coverImage: book.cover_image ? `${this.apiBaseUrl}${book.cover_image}` : null,
          icon: '📚',
          description: book.description || 'Kitob haqida ma\'lumot'
        }));
        
        currentBooks = apiBooks.length > 0 ? apiBooks : [...sampleBooks];
        filteredBooks = [...currentBooks];
      } else {
        console.warn('API dan ma\'lumot olishda xatolik, sample ma\'lumotlar ishlatilmoqda');
        currentBooks = [...sampleBooks];
        filteredBooks = [...sampleBooks];
      }
    } catch (error) {
      console.error('API xatosi:', error);
      currentBooks = [...sampleBooks];
      filteredBooks = [...sampleBooks];
    }
  }
  
  setupFilters() {
    this.filterTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        // Remove active class from all tabs
        this.filterTabs.forEach(t => t.classList.remove('active'));
        // Add active class to clicked tab
        tab.classList.add('active');
        
        // Filter books
        const filter = tab.dataset.filter;
        this.filterBooks(filter);
      });
    });
  }
  
  filterBooks(filter) {
    if (filter === 'all') {
      filteredBooks = [...currentBooks];
    } else {
      filteredBooks = currentBooks.filter(book => book.category === filter);
    }
    
    this.displayBooks(filteredBooks);
    showNotification(`${filteredBooks.length} ta kitob ko'rsatilmoqda`);
  }
  
  displayBooks(books) {
    if (!this.booksContainer) return;
    
    this.booksContainer.innerHTML = '';
    
    books.forEach((book, index) => {
      const bookElement = this.createBookElement(book);
      this.booksContainer.appendChild(bookElement);
      
      // Add staggered animation
      setTimeout(() => {
        bookElement.classList.add('fade-in-up');
      }, index * 100);
    });
  }
  
  createBookElement(book) {
    const discount = calculateDiscount(book.originalPrice, book.price);
    const isInCart = cart.some(item => item.id === book.id);
    const isInFavorites = favorites.some(item => item.id === book.id);
    
    const bookElement = document.createElement('div');
    bookElement.className = 'book-item';
    bookElement.innerHTML = `
      <div class="book-cover-wrapper">
        ${book.coverImage ? 
          `<img src="${book.coverImage}" alt="${book.title}" class="book-cover-image" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
           <div class="book-cover-placeholder ${book.cover}" style="display:none;">${book.icon}</div>` :
          `<div class="book-cover-placeholder ${book.cover}">${book.icon}</div>`
        }
        <div class="book-actions">
          <button class="book-action-btn favorite-btn ${isInFavorites ? 'active' : ''}" 
                  onclick="bookManager.toggleFavorite(${book.id})" 
                  title="Sevimli qo'shish">
            <i class="fas fa-heart"></i>
          </button>
          <button class="book-action-btn quick-view-btn" 
                  onclick="bookManager.quickView(${book.id})" 
                  title="Tez ko'rish">
            <i class="fas fa-eye"></i>
          </button>
          <button class="book-action-btn share-btn" 
                  onclick="bookManager.shareBook(${book.id})" 
                  title="Ulashish">
            <i class="fas fa-share-alt"></i>
          </button>
        </div>
      </div>
      <div class="book-info">
        <div class="book-category">${this.getCategoryName(book.category)}</div>
        <h3 class="book-title">${book.title}</h3>
        <p class="book-author">${book.author}</p>
        <div class="book-rating">
          <div class="rating-stars">${generateStars(book.rating)}</div>
          <span class="rating-count">(${book.ratingCount})</span>
        </div>
        <div class="book-price">
          <span class="price-current">${formatPrice(book.price)}</span>
          <span class="price-original">${formatPrice(book.originalPrice)}</span>
          <span class="price-discount">-${discount}%</span>
        </div>
        <button class="add-to-cart-btn ${isInCart ? 'in-cart' : ''}" 
                onclick="bookManager.toggleCart(${book.id})">
          <i class="fas fa-${isInCart ? 'check' : 'shopping-cart'}"></i>
          ${isInCart ? 'Savatda' : 'Savatga qo\'shish'}
        </button>
      </div>
    `;
    
    return bookElement;
  }
  
  getCategoryName(category) {
    const categoryNames = {
      'all': 'Barchasi',
      'klassik': 'Klassik',
      'zamonaviy': 'Zamonaviy',
      'yoshlar': 'Yoshlar',
      'texnik': 'Texnik',
      'dostoner': 'Doston',
      'sherlar': 'She\'rlar'
    };
    
    return categoryNames[category] || category;
  }
  
  toggleCart(bookId) {
    const book = sampleBooks.find(b => b.id === bookId);
    if (!book) return;
    
    const existingIndex = cart.findIndex(item => item.id === bookId);
    
    if (existingIndex > -1) {
      cart.splice(existingIndex, 1);
      showNotification(`"${book.title}" savatdan o'chirildi`, 'success');
    } else {
      cart.push({ ...book, quantity: 1 });
      showNotification(`"${book.title}" savatga qo'shildi`, 'success');
    }
    
    navigation.updateBadges();
    this.displayBooks(filteredBooks); // Refresh display
  }
  
  toggleFavorite(bookId) {
    const book = sampleBooks.find(b => b.id === bookId);
    if (!book) return;
    
    const existingIndex = favorites.findIndex(item => item.id === bookId);
    
    if (existingIndex > -1) {
      favorites.splice(existingIndex, 1);
      showNotification(`"${book.title}" sevimlilardan o'chirildi`);
    } else {
      favorites.push(book);
      showNotification(`"${book.title}" sevimlilarga qo'shildi`);
    }
    
    navigation.updateBadges();
    this.displayBooks(filteredBooks); // Refresh display
  }
  
  quickView(bookId) {
    const book = sampleBooks.find(b => b.id === bookId);
    if (!book) return;
    
    // Create modal for quick view
    const modal = document.createElement('div');
    modal.className = 'quick-view-modal';
    modal.innerHTML = `
      <div class="modal-overlay" onclick="this.parentElement.remove()"></div>
      <div class="modal-content">
        <button class="modal-close" onclick="this.closest('.quick-view-modal').remove()">
          <i class="fas fa-times"></i>
        </button>
        <div class="quick-view-content">
          <div class="book-preview">
            <div class="book-cover-large ${book.cover}">${book.icon}</div>
          </div>
          <div class="book-details">
            <div class="book-category">${this.getCategoryName(book.category)}</div>
            <h2>${book.title}</h2>
            <p class="author">Muallif: ${book.author}</p>
            <div class="rating-section">
              <div class="rating-stars">${generateStars(book.rating)}</div>
              <span>(${book.ratingCount} baho)</span>
            </div>
            <p class="description">${book.description}</p>
            <div class="price-section">
              <span class="current-price">${formatPrice(book.price)}</span>
              <span class="original-price">${formatPrice(book.originalPrice)}</span>
              <span class="discount">-${calculateDiscount(book.originalPrice, book.price)}%</span>
            </div>
            <div class="action-buttons">
              <button class="btn btn-primary" onclick="bookManager.toggleCart(${book.id}); this.closest('.quick-view-modal').remove();">
                <i class="fas fa-shopping-cart"></i>
                Savatga qo'shish
              </button>
              <button class="btn btn-outline" onclick="bookManager.toggleFavorite(${book.id})">
                <i class="fas fa-heart"></i>
                Sevimli
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
    
    // Add modal styles
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
    
    // Remove modal when clicking outside
    modal.querySelector('.modal-overlay').addEventListener('click', () => {
      document.body.removeChild(modal);
      document.body.style.overflow = '';
    });
  }
  
  shareBook(bookId) {
    const book = sampleBooks.find(b => b.id === bookId);
    if (!book) return;
    
    if (navigator.share) {
      navigator.share({
        title: book.title,
        text: `${book.author} tomonidan yozilgan "${book.title}" kitobini ko'ring`,
        url: window.location.href
      });
    } else {
      // Fallback to clipboard
      const shareText = `${book.title} - ${book.author}\n${window.location.href}`;
      navigator.clipboard.writeText(shareText).then(() => {
        showNotification('Kitob havolasi nusxalandi!');
      });
    }
  }
  
  setupLoadMore() {
    if (this.loadMoreBtn) {
      this.loadMoreBtn.addEventListener('click', () => {
        // Simulate loading more books
        showNotification('Qo\'shimcha kitoblar yuklanmoqda...');
        
        setTimeout(() => {
          // Add more books to display (in real app, this would be an API call)
          const moreBooks = [...sampleBooks].map(book => ({
            ...book,
            id: book.id + 100,
            title: book.title + ' (2-qism)'
          }));
          
          currentBooks = [...currentBooks, ...moreBooks];
          this.filterBooks(document.querySelector('.filter-tab.active').dataset.filter);
        }, 1000);
      });
    }
  }
}

// ==========================================
// ANIMATIONS & EFFECTS
// ==========================================
class AnimationManager {
  constructor() {
    this.init();
  }
  
  init() {
    this.setupScrollAnimations();
    this.setupBackToTop();
    this.setupLoadingScreen();
    this.setupHoverEffects();
  }
  
  setupScrollAnimations() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in-up');
        }
      });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.category-card, .section-header, .card').forEach(el => {
      observer.observe(el);
    });
  }
  
  setupBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    
    if (backToTopBtn) {
      window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
          backToTopBtn.classList.add('visible');
        } else {
          backToTopBtn.classList.remove('visible');
        }
      });
      
      backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }
  }
  
  setupLoadingScreen() {
    const loadingScreen = document.querySelector('.loading-screen');
    
    if (loadingScreen) {
      window.addEventListener('load', () => {
        setTimeout(() => {
          loadingScreen.classList.add('hidden');
          setTimeout(() => {
            loadingScreen.remove();
          }, 500);
        }, 1000);
      });
    }
  }
  
  setupHoverEffects() {
    // Add dynamic hover effects to cards
    document.querySelectorAll('.category-card').forEach(card => {
      card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-8px) scale(1.02)';
      });
      
      card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
      });
    });
  }
}

// ==========================================
// NEWSLETTER SUBSCRIPTION
// ==========================================
class Newsletter {
  constructor() {
    this.form = document.querySelector('.newsletter-form');
    this.emailInput = document.querySelector('.newsletter-email');
    this.submitBtn = document.querySelector('.newsletter-submit');
    
    this.init();
  }
  
  init() {
    if (this.form) {
      this.form.addEventListener('submit', (e) => {
        e.preventDefault();
        this.subscribe();
      });
    }
  }
  
  subscribe() {
    const email = this.emailInput.value.trim();
    
    if (!email) {
      showNotification('Iltimos, email manzilini kiriting', 'error');
      return;
    }
    
    if (!this.validateEmail(email)) {
      showNotification('Noto\'g\'ri email manzil', 'error');
      return;
    }
    
    // Simulate subscription
    this.submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Yuklanmoqda...';
    this.submitBtn.disabled = true;
    
    setTimeout(() => {
      showNotification('Muvaffaqiyatli obuna bo\'ldingiz! Rahmat!');
      this.emailInput.value = '';
      this.submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Obuna bo\'lish';
      this.submitBtn.disabled = false;
    }, 2000);
  }
  
  validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

// ==========================================
// BESTSELLERS
// ==========================================
class Bestsellers {
  constructor() {
    this.container = document.querySelector('.bestsellers-list');
    this.apiBaseUrl = 'http://127.0.0.1:8000';
    this.init();
  }
  
  async init() {
    if (this.container) {
      await this.displayBestsellers();
    }
  }
  
  async displayBestsellers() {
    try {
      // Try to get from API first
      const response = await fetch(`${this.apiBaseUrl}/api/books/books/?ordering=-rating&page_size=5`);
      if (response.ok) {
        const data = await response.json();
        const bestsellers = data.results.slice(0, 5).map(book => ({
          id: book.id,
          title: book.title,
          author: book.author.name,
          rating: parseFloat(book.rating),
          ratingCount: book.review_count,
          price: parseFloat(book.price),
          cover: 'book-cover',
          coverImage: book.cover_image ? `${this.apiBaseUrl}${book.cover_image}` : null,
          icon: '📚'
        }));
        
        this.renderBestsellers(bestsellers);
      } else {
        // Fallback to sample data
        this.renderBestsellers(sampleBooks.sort((a, b) => b.rating - a.rating).slice(0, 5));
      }
    } catch (error) {
      console.error('Bestsellers yuklanmadi:', error);
      // Fallback to sample data
      this.renderBestsellers(sampleBooks.sort((a, b) => b.rating - a.rating).slice(0, 5));
    }
  }
  
  renderBestsellers(bestsellers) {
    this.container.innerHTML = '';
    
    bestsellers.forEach((book, index) => {
      const bestsellerElement = document.createElement('div');
      bestsellerElement.className = 'bestseller-item';
      bestsellerElement.innerHTML = `
        <div class="bestseller-rank">${index + 1}</div>
        ${book.coverImage ?
          `<img src="${book.coverImage}" alt="${book.title}" class="bestseller-cover-img" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';" />
           <div class="bestseller-cover ${book.cover}" style="display:none;">${book.icon}</div>` :
          `<div class="bestseller-cover ${book.cover}">${book.icon}</div>`
        }
        <div class="bestseller-info">
          <h3 class="bestseller-title">${book.title}</h3>
          <p class="bestseller-author">${book.author}</p>
          <div class="bestseller-stats">
            <div class="bestseller-rating">
              <div class="rating-stars">${generateStars(book.rating)}</div>
              <span>(${book.ratingCount})</span>
            </div>
            <div class="bestseller-price">${formatPrice(book.price)}</div>
          </div>
        </div>
      `;
      
      bestsellerElement.addEventListener('click', () => {
        bookManager.quickView(book.id);
      });
      
      this.container.appendChild(bestsellerElement);
    });
  }
}

// ==========================================
// THEME MANAGER
// ==========================================
class ThemeManager {
  constructor() {
    this.currentTheme = localStorage.getItem('theme') || 'light';
    this.init();
  }
  
  init() {
    this.applyTheme();
    this.setupThemeToggle();
  }
  
  applyTheme() {
    document.documentElement.setAttribute('data-theme', this.currentTheme);
    
    if (this.currentTheme === 'dark') {
      document.documentElement.style.setProperty('--bg-primary', '#111827');
      document.documentElement.style.setProperty('--bg-secondary', '#1f2937');
      document.documentElement.style.setProperty('--text-primary', '#f9fafb');
      document.documentElement.style.setProperty('--text-secondary', '#d1d5db');
    }
  }
  
  toggleTheme() {
    this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.currentTheme);
    this.applyTheme();
  }
  
  setupThemeToggle() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', () => {
        this.toggleTheme();
      });
    }
  }
}

// ==========================================
// INITIALIZATION
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
  // Initialize all managers
  window.navigation = new Navigation();
  window.bookManager = new BookManager();
  window.animationManager = new AnimationManager();
  window.newsletter = new Newsletter();
  window.bestsellers = new Bestsellers();
  window.themeManager = new ThemeManager();
  
  // Initialize user authentication UI
  initUserMenu();
  
  console.log('BookNest initialized successfully!');
});

// ==========================================
// USER AUTHENTICATION UI
// ==========================================
function initUserMenu() {
  const userBtn = document.getElementById('userBtn');
  const userDropdown = document.getElementById('userDropdown');
  const userMenuContainer = document.getElementById('userMenuContainer');
  const guestMenu = document.getElementById('guestMenu');
  const authMenu = document.getElementById('authMenu');
  const logoutBtn = document.getElementById('logoutBtn');
  const userName = document.getElementById('userName');
  const userEmail = document.getElementById('userEmail');
  
  // Toggle dropdown on click
  if (userBtn && userDropdown) {
    userBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      userDropdown.classList.toggle('active');
      checkAuthStatus(); // Update status when opening
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!userMenuContainer.contains(e.target)) {
        userDropdown.classList.remove('active');
      }
    });
  }
  
  // Check if user is authenticated
  checkAuthStatus();
  
  // Logout handler
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async function(e) {
      e.preventDefault();
      
      if (window.auth && typeof window.auth.logout === 'function') {
        await window.auth.logout();
      } else {
        // Fallback if auth.js is not loaded
        localStorage.removeItem('authToken');
        localStorage.removeItem('userId');
        localStorage.removeItem('username');
        sessionStorage.removeItem('authToken');
        sessionStorage.removeItem('userId');
        sessionStorage.removeItem('username');
        
        showNotification('Tizimdan chiqdingiz');
        checkAuthStatus();
      }
    });
  }
  
  function checkAuthStatus() {
    const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    const username = localStorage.getItem('username') || sessionStorage.getItem('username');
    const email = localStorage.getItem('userEmail') || sessionStorage.getItem('userEmail');
    
    if (token && username) {
      // User is logged in
      if (guestMenu) guestMenu.style.display = 'none';
      if (authMenu) authMenu.style.display = 'block';
      if (userName) userName.textContent = username;
      if (userEmail) userEmail.textContent = email || username + '@booknest.uz';
    } else {
      // User is not logged in
      if (guestMenu) guestMenu.style.display = 'block';
      if (authMenu) authMenu.style.display = 'none';
    }
  }
  
  // Re-check auth status every time dropdown is opened
  if (userBtn && userDropdown) {
    userBtn.addEventListener('click', function() {
      checkAuthStatus();
    });
  }
}

// ==========================================
// MODAL STYLES (INJECTED)
// ==========================================
const modalStyles = `
<style>
.quick-view-modal .modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
}

.quick-view-modal .modal-content {
  position: relative;
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.quick-view-modal .modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: var(--bg-secondary);
  border: none;
  border-radius: var(--radius-full);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition-fast);
  z-index: 1;
}

.quick-view-modal .modal-close:hover {
  background: var(--error-color);
  color: var(--text-white);
}

.quick-view-modal .quick-view-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2xl);
  padding: var(--space-2xl);
}

.quick-view-modal .book-preview {
  display: flex;
  align-items: center;
  justify-content: center;
}

.quick-view-modal .book-cover-large {
  width: 200px;
  height: 280px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  color: var(--text-white);
  box-shadow: var(--shadow-xl);
}

.quick-view-modal .book-details h2 {
  font-size: 1.5rem;
  margin-bottom: var(--space-sm);
}

.quick-view-modal .author {
  color: var(--text-secondary);
  margin-bottom: var(--space-md);
}

.quick-view-modal .rating-section {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
}

.quick-view-modal .description {
  margin-bottom: var(--space-lg);
  line-height: 1.6;
}

.quick-view-modal .price-section {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}

.quick-view-modal .current-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.quick-view-modal .original-price {
  color: var(--text-light);
  text-decoration: line-through;
}

.quick-view-modal .discount {
  background: var(--success-color);
  color: var(--text-white);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 600;
}

.quick-view-modal .action-buttons {
  display: flex;
  gap: var(--space-md);
}

@media (max-width: 768px) {
  .quick-view-modal .quick-view-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .quick-view-modal .action-buttons {
    flex-direction: column;
  }
}
</style>
`;

// Inject modal styles
if (!document.querySelector('#modal-styles')) {
  const styleElement = document.createElement('div');
  styleElement.id = 'modal-styles';
  styleElement.innerHTML = modalStyles;
  document.head.appendChild(styleElement);
}

// ==========================================
// EXPORT FOR GLOBAL ACCESS
// ==========================================
window.BookNest = {
  cart,
  favorites,
  sampleBooks,
  formatPrice,
  showNotification,
  calculateDiscount
};