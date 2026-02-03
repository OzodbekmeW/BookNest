# 📚 BookNest - E-commerce Book Store

<div align="center">

![BookNest Logo](frontend/images/logo.png)

**A modern, full-stack e-commerce platform for buying and selling books online**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-teal.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## ✨ Features

### 🛍️ Customer Features
- **Browse & Search**: Advanced search and filtering across 1000s of books
- **User Authentication**: Secure JWT-based authentication system
- **Shopping Cart**: Add, update, and manage books in cart
- **Wishlist**: Save favorite books for later
- **Order Management**: Complete checkout flow with order tracking
- **Reviews & Ratings**: Read and write book reviews
- **Multiple Addresses**: Save and manage shipping addresses
- **Responsive Design**: Mobile-first, works on all devices

### 👨‍💼 Admin Features
- **Django Admin Panel**: Comprehensive management interface
- **Inventory Management**: Track stock levels and pricing
- **Order Processing**: View and update order status
- **User Management**: Manage customer accounts
- **Coupon System**: Create and manage discount coupons
- **Analytics Dashboard**: Sales and performance metrics

### 🔧 Technical Features
- RESTful API with FastAPI
- JWT token authentication
- Image uploads and management
- Advanced filtering and pagination
- Email notifications
- Security best practices
- Database optimization with indexes
- Clean, maintainable code

## 🏗️ Project Structure

```
Book_Nest/
├── backend/
│   ├── django_project/          # Django settings and configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── users/                   # User authentication app
│   │   ├── models.py           # User, Address models
│   │   ├── admin.py
│   │   └── ...
│   ├── books/                   # Books catalog app
│   │   ├── models.py           # Book, Category, Author, Cart, Wishlist
│   │   ├── admin.py
│   │   └── ...
│   ├── orders/                  # Order management app
│   │   ├── models.py           # Order, OrderItem, Coupon
│   │   ├── admin.py
│   │   └── ...
│   ├── reviews/                 # Reviews and ratings app
│   │   ├── models.py           # Review model
│   │   ├── admin.py
│   │   └── ...
│   ├── fastapi_app/            # FastAPI application
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── routes/             # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── books.py
│   │   │   └── ...
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── dependencies.py     # Auth dependencies
│   │   └── utils.py
│   ├── media/                  # User uploads
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── index.html              # Homepage
│   ├── catalog.html            # Book listing page
│   ├── book-detail.html        # Book detail page
│   ├── cart.html               # Shopping cart
│   ├── checkout.html           # Checkout flow
│   ├── dashboard.html          # User dashboard
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── about.html              # About page
│   ├── contact.html            # Contact page
│   ├── css/
│   │   ├── variables.css       # CSS custom properties
│   │   ├── reset.css           # CSS reset
│   │   ├── global.css          # Global styles
│   │   ├── components.css      # Reusable components
│   │   └── ...
│   ├── js/
│   │   ├── config.js           # API configuration
│   │   ├── api.js              # API calls
│   │   ├── auth.js             # Authentication logic
│   │   ├── cart.js             # Cart management
│   │   ├── utils.js            # Utility functions
│   │   └── ...
│   └── images/
│
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- PostgreSQL (optional, SQLite for development)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/booknest.git
cd booknest/backend
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env file with your settings
```

Important `.env` variables:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development, PostgreSQL for production)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:8000
```

5. **Run database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (admin)**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python manage.py loaddata sample_data.json
```

8. **Start Django development server**
```bash
python manage.py runserver
```
Django admin will be available at: `http://localhost:8000/admin`

9. **Start FastAPI server (in a new terminal)**
```bash
cd backend/fastapi_app
uvicorn main:app --reload --port 8001
```
FastAPI docs will be available at: `http://localhost:8001/api/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Serve with a local server**

Option 1 - Python HTTP Server:
```bash
python -m http.server 3000
```

Option 2 - Node.js http-server:
```bash
npx http-server -p 3000
```

Option 3 - VS Code Live Server extension

3. **Access the application**
```
http://localhost:3000
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile
- `POST /api/auth/change-password` - Change password
- `POST /api/auth/addresses` - Create address
- `GET /api/auth/addresses` - Get user addresses

### Books
- `GET /api/books/` - List books (with filters & pagination)
- `GET /api/books/{id}` - Get book detail
- `GET /api/books/featured` - Get featured books
- `GET /api/books/bestsellers` - Get bestsellers
- `GET /api/books/new-arrivals` - Get new arrivals
- `GET /api/books/related/{id}` - Get related books

### Categories
- `GET /api/categories/` - List all categories
- `GET /api/categories/{slug}` - Get category detail

### Cart
- `GET /api/cart/` - Get user cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update/{item_id}` - Update cart item
- `DELETE /api/cart/remove/{item_id}` - Remove from cart
- `DELETE /api/cart/clear` - Clear cart

### Wishlist
- `GET /api/wishlist/` - Get wishlist
- `POST /api/wishlist/add` - Add to wishlist
- `DELETE /api/wishlist/remove/{id}` - Remove from wishlist

### Orders
- `POST /api/orders/create` - Create order
- `GET /api/orders/` - Get order history
- `GET /api/orders/{id}` - Get order detail
- `PUT /api/orders/{id}/cancel` - Cancel order

### Reviews
- `POST /api/reviews/create` - Submit review
- `GET /api/reviews/book/{book_id}` - Get book reviews
- `PUT /api/reviews/{id}` - Update review
- `DELETE /api/reviews/{id}` - Delete review

Full API documentation: `http://localhost:8001/api/docs`

## 🗄️ Database Schema

### Core Models

**User** - Custom user model
- username, email, password (hashed)
- phone, avatar, date_of_birth
- is_email_verified, timestamps

**Book** - Book catalog
- title, subtitle, ISBN, description
- author (FK), category (FK), publisher (FK)
- price, discount_price, stock
- images, rating, review_count, view_count
- is_featured, is_bestseller, is_active

**Category** - Book categories (hierarchical)
- name, slug, description, icon
- parent (self-referencing FK)

**Author** - Book authors
- name, bio, photo, nationality

**Order** - Customer orders
- order_number, user (FK), shipping_address (FK)
- subtotal, shipping_cost, discount, total
- status, payment_method, tracking_number

**Review** - Book reviews
- user (FK), book (FK), rating, title, comment
- is_verified_purchase, helpful_count

## 🎨 Frontend Features

### Design System
- **Color Palette**: Professional navy blue & warm red
- **Typography**: Poppins (primary) + Playfair Display (accent)
- **Responsive**: Mobile-first breakpoints
- **Components**: Reusable UI components
- **Animations**: Smooth transitions and micro-interactions

### Key Pages
1. **Homepage** - Hero, featured books, categories, bestsellers
2. **Catalog** - Advanced filtering, sorting, pagination
3. **Book Detail** - Images, reviews, related books
4. **Cart** - Item management, price calculation
5. **Checkout** - Multi-step process
6. **Dashboard** - Orders, wishlist, profile

## 🔐 Security Features

- Password hashing with bcrypt
- JWT token authentication
- CSRF protection
- SQL injection protection (ORM)
- XSS protection
- Input validation
- Rate limiting
- Secure cookie settings
- Environment variables for secrets

## 🧪 Testing

```bash
# Run Django tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📦 Deployment

### Production Settings

1. **Update .env for production**
```env
DEBUG=False
SECRET_KEY=use-strong-random-key
ALLOWED_HOSTS=yourdomain.com
DB_ENGINE=django.db.backends.postgresql
```

2. **Collect static files**
```bash
python manage.py collectstatic
```

3. **Use production server**
- Gunicorn for Django
- Uvicorn for FastAPI
- Nginx as reverse proxy

4. **Database**
- PostgreSQL for production
- Regular backups

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django & FastAPI communities
- Font Awesome for icons
- Google Fonts for typography
- All contributors and testers

## 📞 Support

For support, email info@booknest.uz or open an issue on GitHub.

---

<div align="center">
Made with ❤️ by BookNest Team
</div>
