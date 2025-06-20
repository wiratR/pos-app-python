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

    # --- Create products table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL
        )
    """)

    # --- Create customers table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            company_address TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            tax_id TEXT NOT NULL UNIQUE
        )
    """)

    # --- Create orders table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT NOT NULL UNIQUE,
            order_date TEXT NOT NULL,
            delivery_date TEXT NOT NULL,
            customer_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            order_payment_status TEXT CHECK(order_payment_status IN ('paid', 'unpaid', 'pending', 'cancelled')) DEFAULT 'unpaid',
            payment_complete_date TEXT DEFAULT '1970-01-01',  -- 🔘 Default คือ 1 มกราคม 1970
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    # --- Create order_items table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # --- Create stock table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL UNIQUE,
            stock_quantity INTEGER NOT NULL DEFAULT 0,
            cost_price REAL NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # Sample product data: [name, description, price]
    sample_data = [
        ("ปูนซีเมนต์ปอร์ตแลนด์", "ใช้สำหรับงานโครงสร้าง", 120.00),
        ("ปูนสำเร็จรูป", "ใช้สำหรับงานก่อฉาบ", 85.50),
        ("ทรายหยาบ", "วัสดุก่อสร้างทั่วไป", 45.00),
        ("หินคลุก", "ถมพื้นที่รองพื้นถนน", 55.00)
    ]

    cursor.executemany(
        "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
        sample_data
    )

    # Insert initial stock data for sample products with cost_price (ตัวอย่างกำหนดต้นทุน)
    # สมมติต้นทุน 80% ของราคาขาย
    cursor.execute("SELECT id, price FROM products")
    products = cursor.fetchall()
    stock_data = []
    for prod_id, price in products:
        cost_price = round(price * 0.8, 2)
        stock_data.append((prod_id, 10, cost_price)) # เริ่มต้น stock 10 

    cursor.executemany(
        "INSERT INTO stock (product_id, stock_quantity, cost_price) VALUES (?, ?, ?)",
        stock_data
    )

    conn.commit()
    conn.close()
    print("✅ Database initialized with tables, sample products, and stock data.")

if __name__ == "__main__":
    initialize_database()
