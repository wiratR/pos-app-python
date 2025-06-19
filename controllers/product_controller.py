import os
import sys
from models.product_model import ProductModel
from utils.path_utils import resource_path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
class ProductController:
    def __init__(self, db_path: str = None):
        if db_path is None:
            env_db_path = os.getenv("DATABASE_PATH", "database/app.sqlite")
            db_path = resource_path(env_db_path)
        self.model = ProductModel(db_path)

    def get_all_products(self):
        return self.model.get_all_products()

    def add_product(self, name: str, description: str, price: float):
        return self.model.add_product(name, description, price)

    def update_product(self, product_id: int, name: str, description: str, price: float):
        return self.model.update_product(product_id, name, description, price)

    def delete_product(self, product_id: int):
        return self.model.delete_product(product_id)
