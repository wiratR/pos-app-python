from models.product_model import ProductModel  # ปรับ path ให้ตรงกับโปรเจกต์ของคุณ

class ProductController:
    def __init__(self, db_path: str = None):
        self.model = ProductModel(db_path)

    def get_all_products(self):
        return self.model.get_all_products()

    def get_product_by_id(self, product_id: int):
        return self.model.get_product_by_id(product_id)

    def get_product_by_name(self, name: str):
        return self.model.get_product_by_name(name)

    def get_product_id_by_name(self, name: str):
        return self.model.get_product_id_by_name(name)

    def get_products_by_price_range(self, min_price: float, max_price: float):
        return self.model.get_products_by_price_range(min_price, max_price)

    def get_product_count(self):
        return self.model.get_product_count()

    def add_product(self, name: str, description: str, price: float):
        if not name or price is None:
            raise ValueError("Product name and price are required.")
        return self.model.add_product(name, description, price)

    def update_product(self, product_id: int, name: str, description: str, price: float):
        if not self.model.get_product_by_id(product_id):
            raise ValueError(f"Product with ID {product_id} does not exist.")
        return self.model.update_product(product_id, name, description, price)

    def delete_product(self, product_id: int):
        if not self.model.get_product_by_id(product_id):
            raise ValueError(f"Product with ID {product_id} does not exist.")
        return self.model.delete_product(product_id)

    def clear_all_products(self):
        self.model.clear_products()
