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

