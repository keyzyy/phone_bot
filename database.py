import sqlite3

# DATABASE ulash
conn = sqlite3.connect("shop.db", check_same_thread=False)
cursor = conn.cursor()

# TABLE yaratish (agar yo‘q bo‘lsa)
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    product TEXT
)
""")

conn.commit()

# BUYURTMA SAQLASH
def save_order(name, phone, product):
    cursor.execute(
        "INSERT INTO orders (name, phone, product) VALUES (?, ?, ?)",
        (name, phone, product)
    )
    conn.commit()

# HAMMA BUYURTMANI OLISH (ADMIN uchun)
def get_orders():
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    return cursor.fetchall()
