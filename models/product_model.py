import os
import sys
import sqlite3
import logging
from typing import List, Dict, Optional
from utils.path_utils import resource_path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ProductModel:
    def __init__(self, db_path: str = None):
        if db_path is None:
            env_db_path = os.getenv("DATABASE_PATH", "database/app.sqlite")
            db_path = resource_path(env_db_path)
        self.db_path = db_path
        # self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL
                )
            """)
            conn.commit()

    def get_all_products(self) -> List[Dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price FROM products")
            rows = cursor.fetchall()
            return [
                {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
                for row in rows
            ]

    def update_product(self, product_id: int, name: str, description: str, price: float) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
                (name, description, price, product_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def add_product(self, name: str, description: str, price: float) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                (name, description, price)
            )
            conn.commit()
            return cursor.lastrowid

    def delete_product(self, product_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return cursor.rowcount > 0
        
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
            return None
        
    def get_product_by_name(self, name: str) -> Optional[Dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price FROM products WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
            return None
        
    def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Dict]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price FROM products WHERE price BETWEEN ? AND ?", (min_price, max_price))
            rows = cursor.fetchall()
            return [
                {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
                for row in rows
            ]
        
    def get_product_count(self) -> int:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            return count
        
    def clear_products(self) -> None:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products")
            conn.commit()
            logging.info("All products cleared from the database.")
    
    def get_product_id_by_name(self, name: str) -> Optional[int]:
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM products WHERE name = ?", (name,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
