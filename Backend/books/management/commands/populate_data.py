"""
Management command to populate database with sample data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from books.models import Category, Author, Publisher, Book
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@booknest.uz',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superuser created'))
        
        # Create Categories
        categories_data = [
            {'name': 'Klassik adabiyot', 'slug': 'klassik', 'icon': 'fa-book-open', 
             'description': 'O\'zbek va jahon klassik asarlari'},
            {'name': 'Zamonaviy adabiyot', 'slug': 'zamonaviy', 'icon': 'fa-star',
             'description': 'Hozirgi zamon yozuvchilarining asarlari'},
            {'name': 'Yoshlar adabiyoti', 'slug': 'yoshlar', 'icon': 'fa-child',
             'description': 'Bolalar va yoshlar uchun kitoblar'},
            {'name': 'Ilmiy-ommabop', 'slug': 'ilmiy', 'icon': 'fa-flask',
             'description': 'Fan va texnologiya bo\'yicha kitoblar'},
            {'name': 'Biznes va iqtisod', 'slug': 'biznes', 'icon': 'fa-chart-line',
             'description': 'Biznes, marketing va moliya'},
            {'name': 'Dasturlash', 'slug': 'dasturlash', 'icon': 'fa-code',
             'description': 'Dasturlash va IT texnologiyalari'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(f'  ✓ Category: {cat.name}')
        
        # Create Authors
        authors_data = [
            {'name': 'Abdulla Qodiriy', 'slug': 'abdulla-qodiriy',
             'bio': 'O\'zbek adabiyotining asoschisi, yirik yozuvchi',
             'nationality': 'O\'zbekiston'},
            {'name': 'Alisher Navoiy', 'slug': 'alisher-navoiy',
             'bio': 'Buyuk o\'zbek shoiri va mutafakkiri',
             'nationality': 'O\'zbekiston'},
            {'name': 'Murod Muhammad Do\'st', 'slug': 'murod-muhammad-dost',
             'bio': 'Zamonaviy o\'zbek yozuvchisi',
             'nationality': 'O\'zbekiston'},
            {'name': 'Said Ahmad', 'slug': 'said-ahmad',
             'bio': 'Yozuvchi, publitsist',
             'nationality': 'O\'zbekiston'},
            {'name': 'Napoleon Hill', 'slug': 'napoleon-hill',
             'bio': 'Amerikalik muallif va motivatsion ma\'ruzachi',
             'nationality': 'AQSH'},
            {'name': 'Dale Carnegie', 'slug': 'dale-carnegie',
             'bio': 'Amerikalik yozuvchi va o\'qituvchi',
             'nationality': 'AQSH'},
        ]
        
        authors = {}
        for auth_data in authors_data:
            auth, created = Author.objects.get_or_create(
                slug=auth_data['slug'],
                defaults=auth_data
            )
            authors[auth_data['slug']] = auth
            if created:
                self.stdout.write(f'  ✓ Author: {auth.name}')
        
        # Create Publishers
        publishers_data = [
            {'name': 'O\'zbekiston', 'slug': 'ozbekiston'},
            {'name': 'Sharq', 'slug': 'sharq'},
            {'name': 'Yangi asr avlodi', 'slug': 'yangi-asr'},
            {'name': 'Tafakkur', 'slug': 'tafakkur'},
        ]
        
        publishers = {}
        for pub_data in publishers_data:
            pub, created = Publisher.objects.get_or_create(
                slug=pub_data['slug'],
                defaults=pub_data
            )
            publishers[pub_data['slug']] = pub
            if created:
                self.stdout.write(f'  ✓ Publisher: {pub.name}')
        
        # Create Books
        books_data = [
            {
                'title': 'O\'tgan kunlar',
                'author': 'abdulla-qodiriy',
                'category': 'klassik',
                'publisher': 'ozbekiston',
                'description': 'O\'zbek adabiyotining ilk romoni. O\'tgan davr hayotidan lavhalar.',
                'price': Decimal('45000'),
                'discount_price': Decimal('40000'),
                'stock': 50,
                'pages': 384,
                'language': 'uz',
                'publication_year': 1926,
                'is_featured': True,
                'is_bestseller': True,
                'rating': Decimal('4.8'),
                'review_count': 256,
                'cover_image': 'books/covers/default.jpg',
            },
            {
                'title': 'Xamsa',
                'author': 'alisher-navoiy',
                'category': 'klassik',
                'publisher': 'sharq',
                'description': 'Alisher Navoiyning besh dostoni to\'plami. Buyuk ijodkor merosi.',
                'price': Decimal('75000'),
                'discount_price': Decimal('65000'),
                'stock': 30,
                'pages': 640,
                'language': 'uz',
                'publication_year': 1485,
                'is_featured': True,
                'is_bestseller': True,
                'rating': Decimal('4.9'),
                'review_count': 342,
                'cover_image': 'books/covers/default.jpg',
            },
            {
                'title': 'Yer yuzidagi eng chiroyli yer',
                'author': 'murod-muhammad-dost',
                'category': 'zamonaviy',
                'publisher': 'yangi-asr',
                'description': 'Zamonaviy o\'zbek adabiyotidan ajoyib asar. Vatan muhabbati haqida.',
                'price': Decimal('42000'),
                'discount_price': Decimal('38000'),
                'stock': 75,
                'pages': 320,
                'language': 'uz',
                'publication_year': 2015,
                'is_featured': True,
                'rating': Decimal('4.7'),
                'review_count': 156,
                'cover_image': 'books/covers/default.jpg',
            },
            {
                'title': 'Baxtli kunlar',
                'author': 'said-ahmad',
                'category': 'yoshlar',
                'publisher': 'tafakkur',
                'description': 'Yoshlar uchun mo\'ljallangan qiziqarli roman. Hayot va muhabbat haqida.',
                'price': Decimal('35000'),
                'discount_price': Decimal('30000'),
                'stock': 100,
                'pages': 256,
                'language': 'uz',
                'publication_year': 2018,
                'is_featured': False,
                'rating': Decimal('4.6'),
                'review_count': 89,
                'cover_image': 'books/covers/default.jpg',
            },
            {
                'title': 'O\'ylab ko\'ring va boy bo\'ling',
                'author': 'napoleon-hill',
                'category': 'biznes',
                'publisher': 'tafakkur',
                'description': 'Shaxsiy rivojlanish bo\'yicha dunyoga mashhur kitob.',
                'price': Decimal('55000'),
                'discount_price': Decimal('48000'),
                'stock': 60,
                'pages': 304,
                'language': 'uz',
                'publication_year': 1937,
                'is_featured': True,
                'is_bestseller': True,
                'rating': Decimal('4.9'),
                'review_count': 512,
                'cover_image': 'books/covers/default.jpg',
            },
            {
                'title': 'Do\'stlarni qanday orttiramiz',
                'author': 'dale-carnegie',
                'category': 'biznes',
                'publisher': 'tafakkur',
                'description': 'Muloqot san\'ati haqida dunyoning eng mashhur kitobi.',
                'price': Decimal('48000'),
                'discount_price': Decimal('42000'),
                'stock': 80,
                'pages': 288,
                'language': 'uz',
                'publication_year': 1936,
                'is_featured': True,
                'is_bestseller': True,
                'rating': Decimal('4.8'),
                'review_count': 428,
                'cover_image': 'books/covers/default.jpg',
            },
        ]
        
        for book_data in books_data:
            author_slug = book_data.pop('author')
            category_slug = book_data.pop('category')
            publisher_slug = book_data.pop('publisher')
            
            book_data['author'] = authors[author_slug]
            book_data['category'] = categories[category_slug]
            book_data['publisher'] = publishers[publisher_slug]
            
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(f'  ✓ Book: {book.title}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data created successfully!'))
        self.stdout.write(self.style.SUCCESS('✓ Admin credentials: admin / admin123'))
