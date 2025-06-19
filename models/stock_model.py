import sqlite3
from utils.path_utils import resource_path
import os

class StockModel:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = resource_path("database/app.sqlite")
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def get_stock_by_product(self, product_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT stock_quantity, cost_price FROM stock WHERE product_id = ?", (product_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"stock_quantity": row[0], "cost_price": row[1]}
        return None

    def add_stock(self, product_id, quantity, cost_price):
        """
        เพิ่มสต็อกใหม่ หรือถ้ามีอยู่แล้วให้ update
        """
        conn = self.connect()
        cursor = conn.cursor()

        existing = self.get_stock_by_product(product_id)
        if existing is None:
            cursor.execute("""
                INSERT INTO stock (product_id, stock_quantity, cost_price) 
                VALUES (?, ?, ?)
            """, (product_id, quantity, cost_price))
        else:
            new_quantity = existing['stock_quantity'] + quantity
            cursor.execute("""
                UPDATE stock SET stock_quantity = ?, cost_price = ? 
                WHERE product_id = ?
            """, (new_quantity, cost_price, product_id))

        conn.commit()
        conn.close()

    def update_stock(self, product_id, quantity=None, cost_price=None):
        """
        อัปเดตสต็อก (stock_quantity หรือ cost_price) อย่างใดอย่างหนึ่งหรือทั้งสอง
        """
        conn = self.connect()
        cursor = conn.cursor()

        updates = []
        params = []

        if quantity is not None:
            updates.append("stock_quantity = ?")
            params.append(quantity)

        if cost_price is not None:
            updates.append("cost_price = ?")
            params.append(cost_price)

        if not updates:
            conn.close()
            return  # ไม่มีอะไรให้อัปเดต

        params.append(product_id)
        sql = f"UPDATE stock SET {', '.join(updates)} WHERE product_id = ?"
        cursor.execute(sql, params)

        conn.commit()
        conn.close()

    def delete_stock(self, product_id):
        """
        ลบข้อมูลสต็อกจากฐานข้อมูลโดยใช้ product_id
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stock WHERE product_id = ?", (product_id,))
        conn.commit()
        conn.close()

    def get_stock_by_product_name(self, name):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.stock_quantity, s.cost_price 
            FROM stock s
            JOIN products p ON s.product_id = p.id
            WHERE p.name = ?
        """, (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"stock_quantity": row[0], "cost_price": row[1]}
        return None