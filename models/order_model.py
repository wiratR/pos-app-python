import os
import sys
import sqlite3
import logging
from datetime import datetime
from utils.path_utils import resource_path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OrderModel:
    def __init__(self, db_path: str = None):
        if db_path is None:
            env_db_path = os.getenv("DATABASE_PATH", "database/app.sqlite")
            db_path = resource_path(env_db_path)
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_or_create_customer(self, company_name, address, contact_name, phone, email, tax_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM customers WHERE tax_id = ?", (tax_id,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row[0]

        cursor.execute("""
            INSERT INTO customers (company_name, company_address, contact_name, phone, email, tax_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (company_name, address, contact_name, phone, email, tax_id))
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return customer_id

    def create_order(self, order_no, order_date, delivery_date, customer_id, total_amount, payment_status='unpaid'):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders (order_no, order_date, delivery_date, customer_id, total_amount, order_payment_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_no, order_date, delivery_date, customer_id, total_amount, payment_status))
        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id

    def add_order_items(self, order_id, items):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany("""
            INSERT INTO order_items (order_id, product_id, quantity, subtotal)
            VALUES (?, ?, ?, ?)
        """, [(order_id, product_id, qty, subtotal) for product_id, qty, subtotal in items])
        conn.commit()
        conn.close()

    def get_all_orders(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                o.order_no, 
                o.order_date, 
                o.delivery_date, 
                c.company_name, 
                o.total_amount,
                o.order_payment_status
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
        """)

        columns = [column[0] for column in cursor.description]
        orders = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return orders

    def update_payment_status(self, order_no, new_status):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE orders
            SET order_payment_status = ?
            WHERE order_no = ?
        """, (new_status, order_no))

        conn.commit()
        conn.close()

    def get_paid_orders(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT orders.order_no, orders.order_date, orders.delivery_date, 
                customers.company_name, orders.total_amount
            FROM orders
            JOIN customers ON orders.customer_id = customers.id
            WHERE order_payment_status = 'paid'
            ORDER BY orders.order_date DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    def get_order_by_no(self, order_no):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                o.order_no,
                o.order_date,
                o.delivery_date,
                o.total_amount,
                c.company_name,
                c.company_address,
                c.contact_name,
                c.phone,
                c.email,
                c.tax_id
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.order_no = ?
        """, (order_no,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "order_no": row[0],
                "order_date": row[1],
                "delivery_date": row[2],
                "total_amount": row[3],
                "company_name": row[4],
                "company_address": row[5],
                "contact_name": row[6],
                "phone": row[7],
                "email": row[8],
                "tax_id": row[9],
            }
        return None

    def get_order_items(self, order_no):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, oi.quantity, oi.subtotal / oi.quantity AS unit_price
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN products p ON oi.product_id = p.id
            WHERE o.order_no = ?
        """, (order_no,))
        items = [{"name": r[0], "quantity": r[1], "unit_price": r[2]} for r in cursor.fetchall()]
        conn.close()
        return items
    
    def get_product_name_by_id(self, product_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else "ไม่ทราบชื่อสินค้า"