#!/bin/bash
# Database Monitor Script
# Ma'lumotlarni real-time kuzatish

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          📊 BOOKNEST DATABASE MONITOR                     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

DB_PATH="/Users/ozodbek_tursunpulatov/Desktop/Python/Book_Nest/Backend/db.sqlite3"

# Users count
USERS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM users_user;")
echo "👥 Foydalanuvchilar: $USERS"

# Tokens count
TOKENS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM authtoken_token;")
echo "🔑 Aktiv tokenlar: $TOKENS"

# Books count
BOOKS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM books_book;")
echo "📚 Kitoblar: $BOOKS"

# Categories count
CATEGORIES=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM books_category;")
echo "📂 Kategoriyalar: $CATEGORIES"

# Orders count
ORDERS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM orders_order;")
echo "🛒 Buyurtmalar: $ORDERS"

# Reviews count
REVIEWS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM reviews_review;")
echo "⭐ Sharhlar: $REVIEWS"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Oxirgi 5 ta foydalanuvchi:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

sqlite3 "$DB_PATH" "
SELECT 
    id || ' │ ' || 
    username || ' │ ' || 
    email || ' │ ' || 
    substr(date_joined, 1, 19) as info
FROM users_user 
ORDER BY id DESC 
LIMIT 5;
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔐 Aktiv tokenlar:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

sqlite3 "$DB_PATH" "
SELECT 
    u.username || ' │ ' || 
    substr(t.key, 1, 20) || '...' || ' │ ' ||
    substr(t.created, 1, 19) as token_info
FROM authtoken_token t
JOIN users_user u ON t.user_id = u.id
ORDER BY t.created DESC
LIMIT 5;
"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Database file:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh "$DB_PATH"
echo ""
