import os
import sys
import sqlite3
import logging
from datetime import datetime

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class OrderModel:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = resource_path(os.path.join("database", "app.sqlite"))
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

    def create_order(self, order_no, order_date, delivery_date, customer_id, total_amount):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders (order_no, order_date, delivery_date, customer_id, total_amount)
            VALUES (?, ?, ?, ?, ?)
        """, (order_no, order_date, delivery_date, customer_id, total_amount))
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
            SELECT o.order_no, o.order_date, o.delivery_date, c.company_name, o.total_amount
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.order_date DESC
        """)

        columns = [column[0] for column in cursor.description]
        orders = [dict(zip(columns, row)) for row in cursor.fetchall()]

        conn.close()
        return orders