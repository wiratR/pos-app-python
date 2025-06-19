from models.stock_model import StockModel

class StockController:
    def __init__(self):
        self.model = StockModel()

    def add_or_update_stock(self, product_id, quantity, cost_price):
        """
        เพิ่มสต็อกใหม่หรืออัปเดตสต็อกและราคาต้นทุน
        """
        self.model.add_stock(product_id, quantity, cost_price)

    def update_stock(self, product_id, quantity=None, cost_price=None):
        """
        อัปเดตสต็อก (ถ้ามีข้อมูลที่ต้องการอัปเดต)
        """
        self.model.update_stock(product_id, quantity, cost_price)

    def delete_stock(self, product_id: int):
        """
        ลบข้อมูลสต็อกจากฐานข้อมูลโดยใช้ product_id
        """
        return self.model.delete_stock(product_id)
    
    def get_stock_by_product(self, product_id):
        """
        ดึงข้อมูลสต็อกโดยใช้ product_id
        """
        return self.model.get_stock_by_product(product_id)
    
    def get_stock_by_product_name(self, product_name):
        """
        ดึงข้อมูลสต็อกโดยใช้ชื่อสินค้า
        """
        return self.model.get_stock_by_product_name(product_name)