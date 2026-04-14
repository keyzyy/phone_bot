import sqlite3

conn = sqlite3.connect("shop.db", check_same_thread=False)
cursor = conn.cursor()

# table yaratish
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    product TEXT
)
""")

conn.commit()

def save_order(name, phone, product):
    cursor.execute(
        "INSERT INTO orders (name, phone, product) VALUES (?, ?, ?)",
        (name, phone, product)
    )
    conn.commit()
