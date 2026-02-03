# 📚 BookNest - Onlayn Kitob Do'koni

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.14-red?style=for-the-badge&logo=django)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

O'zbek tilida ishlaydigan zamonaviy kitob savdo platformasi. Django backend va vanilla JavaScript frontend bilan qurilgan.

## ✨ Imkoniyatlar

- 🔐 Foydalanuvchi autentifikatsiyasi (JWT)
- 📖 Kitoblarni kategoriya bo'yicha ko'rish va filtrlash
- 🔍 Kitob qidirish
- ⭐ Sevimlilar ro'yxati
- 🛒 Savat tizimi
- 💳 Buyurtma berish
- 📱 Responsive dizayn (mobil va desktop)
- 🖼️ Kitob rasmlari bilan

## 🛠️ Texnologiyalar

### Backend
- Django 5.0.2
- Django REST Framework
- JWT Authentication (SimpleJWT)
- SQLite Database
- Pillow (rasm ishlash)
- CORS Headers

### Frontend
- HTML5
- CSS3 (Vanilla CSS)
- JavaScript (Vanilla JS)
- Font Awesome Icons
- Google Fonts

## 📦 O'rnatish

### 1. Repositoriyani clone qiling

```bash
git clone https://github.com/OzodbekmeW/BookNest.git
cd BookNest
```

### 2. Virtual environment yarating

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# yoki
.venv\Scripts\activate  # Windows
```

### 3. Dependencies o'rnating

```bash
pip install -r Backend/requirements.txt
```

### 4. Database migratsiyalarini bajaring

```bash
cd Backend
python manage.py migrate
```

### 5. Sample ma'lumotlar yuklang (ixtiyoriy)

```bash
python manage.py shell
>>> from books.management.commands.populate_data import Command
>>> Command().handle()
>>> exit()
```

### 6. Superuser yarating (ixtiyoriy)

```bash
python manage.py createsuperuser
```

### 7. Backend serverni ishga tushiring

```bash
python manage.py runserver
```

Backend `http://127.0.0.1:8000` da ishga tushadi.

### 8. Frontend serverni ishga tushiring

Yangi terminal oching:

```bash
cd Frontend
python3 -m http.server 3000
```

Frontend `http://localhost:3000` da ochiladi.

## 📁 Loyiha Tuzilishi

```
BookNest/
├── Backend/
│   ├── django_project/     # Asosiy sozlamalar
│   │   ├── settings.py     # Django sozlamalari
│   │   ├── urls.py         # URL routerlar
│   │   └── wsgi.py         # WSGI konfiguratsiya
│   │
│   ├── books/              # Kitoblar moduli
│   │   ├── models.py       # Book, Category, Author, Cart, Wishlist
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   ├── urls.py         # Books URLs
│   │   └── admin.py        # Admin panel
│   │
│   ├── users/              # Foydalanuvchilar moduli
│   │   ├── models.py       # User, UserProfile
│   │   ├── views.py        # Auth views
│   │   ├── serializers.py  # User serializers
│   │   └── urls.py         # Auth URLs
│   │
│   ├── orders/             # Buyurtmalar moduli
│   │   ├── models.py       # Order, OrderItem
│   │   ├── views.py        # Order views
│   │   └── admin.py        # Order admin
│   │
│   ├── reviews/            # Sharhlar moduli
│   │   ├── models.py       # Review, Rating
│   │   └── views.py        # Review views
│   │
│   ├── media/              # Yuklangan fayllar
│   │   └── books/covers/   # Kitob rasmlari
│   │
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   └── db.sqlite3          # SQLite database
│
└── Frontend/
    ├── index.html          # Asosiy sahifa
    ├── login.html          # Kirish sahifasi
    ├── signup.html         # Ro'yxatdan o'tish
    ├── style.css           # Asosiy CSS
    ├── auth.css            # Auth CSS
    ├── script.js           # Asosiy JavaScript
    ├── auth.js             # Auth JavaScript
    └── api.js              # API client
```

## 🔧 API Endpoints

### Authentication
```
POST /api/auth/register/    # Ro'yxatdan o'tish
POST /api/auth/login/       # Kirish
POST /api/auth/logout/      # Chiqish
```

### Books
```
GET    /api/books/books/           # Barcha kitoblar
GET    /api/books/books/{id}/      # Bitta kitob
GET    /api/books/categories/      # Kategoriyalar
GET    /api/books/authors/         # Mualliflar
POST   /api/books/cart/            # Savatga qo'shish
GET    /api/books/wishlist/        # Sevimlilar
```

### Admin
```
GET /admin/    # Django admin panel
```

## 🌟 Asosiy Xususiyatlar

### Kategoriyalar
- Klassik adabiyot
- Zamonaviy adabiyot
- Biznes va iqtisod
- Yoshlar adabiyoti
- Dasturlash
- Ilmiy-ommabop

### Filtrlash
- Kategoriya bo'yicha
- Narx diapazoni
- Reyting bo'yicha
- Muallif bo'yicha

### Qidirish
- Kitob nomi bo'yicha
- Muallif nomi bo'yicha
- Kategoriya bo'yicha

### Responsive Dizayn
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🚀 Production uchun

### Static fayllarni to'plash

```bash
python manage.py collectstatic --noinput
```

### Gunicorn bilan ishga tushirish

```bash
pip install gunicorn
gunicorn django_project.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables

`.env` fayl yarating va quyidagilarni sozlang:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=your-database-url
```

## 📸 Screenshots

### Asosiy Sahifa
- Hero section
- Kategoriyalar
- Tavsiya etilgan kitoblar
- Bestsellers

### Kitob Detallari
- Kitob rasmi
- Tavsif
- Narx
- Reyting va sharhlar

### Autentifikatsiya
- Kirish
- Ro'yxatdan o'tish
- User dropdown menu

## 🤝 Hissa Qo'shish

Pull requestlar qabul qilinadi! Katta o'zgarishlar uchun avval issue oching.

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. Commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

## 📝 Litsenziya

MIT License

## 👨‍💻 Muallif

**Ozodbek Tursunpulatov**

- Email: ozodbekt2600@gmail.com
- GitHub: [@OzodbekmeW](https://github.com/OzodbekmeW)

## 🙏 Minnatdorchilik

- Django va DRF jamoasiga
- Open source community ga
- Barcha contributors ga

---

⭐ Agar loyiha yoqsa, star bosing!

💬 Savol yoki takliflar bo'lsa, issue oching!

🚀 Happy Coding!
