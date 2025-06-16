import sqlite3
import os

def initialize_database():
    db_path = os.path.join("database", "app.sqlite")
    os.makedirs("database", exist_ok=True)

    if os.path.exists(db_path):
        print("✅ Database already exists. Skipping initialization.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
    """)

    # 👇 Sample product data: [name, description, price]
    sample_data = [
        ("ปูนซีเมนต์ปอร์ตแลนด์", "ใช้สำหรับงานโครงสร้าง", 120.00),
        ("ปูนสำเร็จรูป", "ใช้สำหรับงานก่อฉาบ", 85.50),
        ("ทรายหยาบ", "วัสดุก่อสร้างทั่วไป", 45.00),
        ("หินคลุก", "ถมพื้นที่รองพื้นถนน", 55.00)
    ]

    cursor.executemany("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()
    conn.close()

    print("✅ Database initialized with sample product data.")

if __name__ == "__main__":
    initialize_database()
