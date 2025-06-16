import os
import sys
from models.product_model import ProductModel

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class ProductController:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = resource_path(os.path.join("database", "app.sqlite"))
        self.model = ProductModel(db_path)

    def get_all_products(self):
        return self.model.get_all_products()

    def add_product(self, name: str, description: str, price: float):
        return self.model.add_product(name, description, price)

    def update_product(self, product_id: int, name: str, description: str, price: float):
        return self.model.update_product(product_id, name, description, price)

    def delete_product(self, product_id: int):
        return self.model.delete_product(product_id)
