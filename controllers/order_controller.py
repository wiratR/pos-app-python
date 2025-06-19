from models.order_model import OrderModel

class OrderController:
    def __init__(self):
        self.model = OrderModel()

    def create_order(self, order_data, items):
        """
        order_data = {
            'order_no': str,
            'order_date': str,         # format: YYYY-MM-DD
            'delivery_date': str,      # format: YYYY-MM-DD
            'company_name': str,
            'company_address': str,
            'contact_name': str,
            'phone': str,
            'email': str,
            'tax_id': str,
            'total_amount': float,
            'payment_status': str      # example: 'paid' or 'unpaid'
        }

        items = List of tuples: [(product_id, quantity, subtotal), ...]
        """
        customer_id = self.model.get_or_create_customer(
            order_data['company_name'],
            order_data['company_address'],
            order_data['contact_name'],
            order_data['phone'],
            order_data['email'],
            order_data['tax_id']
        )

        # ใช้ 'unpaid' เป็นค่า default หากไม่ส่ง payment_status มา
        payment_status = order_data.get('payment_status', 'unpaid')

        order_id = self.model.create_order(
            order_data['order_no'],
            order_data['order_date'],
            order_data['delivery_date'],
            customer_id,
            order_data['total_amount'],
            payment_status
        )

        self.model.add_order_items(order_id, items)
        return order_id

    def get_all_orders(self):
        return self.model.get_all_orders()
    
    def update_payment_status(self, order_no, new_status):
        """
        อัปเดตสถานะการชำระเงินของคำสั่งซื้อ
        :param order_no: str - เลขที่คำสั่งซื้อ
        :param new_status: str - สถานะใหม่ เช่น 'paid' หรือ 'unpaid'
        """
        self.model.update_payment_status(order_no, new_status)

    def get_paid_orders(self):
        """
        ดึงรายการคำสั่งซื้อที่ชำระเงินแล้ว
        :return: List of tuples - รายการคำสั่งซื้อที่ชำระเงินแล้ว
        """
        return self.model.get_paid_orders()
    
    
    def get_order_by_no(self, order_no):
        """
        ดึงรายละเอียดคำสั่งซื้อรวมถึงรายการสินค้า
        :param order_no: str - เลขที่คำสั่งซื้อ
        :return: dict - ข้อมูลคำสั่งซื้อพร้อมรายการสินค้า
        """
        order = self.model.get_order_by_no(order_no)
        items = self.model.get_order_items(order_no)
        order['items'] = items
        return order
    
    def get_order_items(self, order_no):
        """
        ดึงรายการสินค้าของคำสั่งซื้อ
        :param order_no: str - เลขที่คำสั่งซื้อ
        :return: List of tuples - รายการสินค้าในคำสั่งซื้อนั้น
        """
        return self.model.get_order_items(order_no)
    
    def get_product_name_by_id(self, product_id):
        """
        ดึงชื่อสินค้าจาก product_id
        :param product_id: int - รหัสสินค้า
        :return: str - ชื่อสินค้า
        """
        return self.model.get_product_name_by_id(product_id)