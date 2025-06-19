from PyQt6.QtCore import QAbstractTableModel, Qt

class OrderTableModel(QAbstractTableModel):
    def __init__(self, orders):
        super().__init__()
        self.orders = orders
        self.headers = ["เลขที่ใบสั่ง", "วันที่สั่ง", "วันที่ส่ง", "ชื่อลูกค้า", "ยอดรวม", "สถานะชำระเงิน", "ใบส่งของ", "ใบเสนอราคา"]

        return None

    def rowCount(self, parent=None):
        return len(self.orders)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            col = index.column()
            order = self.orders[index.row()]
            if col == 5:
                return order.get("order_payment_status", "ยังไม่ชำระ")
            elif col == 6:
                return "ใบส่งของ"
            elif col == 7:
                return "ใบเสนอราคา"
            else:
                keys = ["order_no", "order_date", "delivery_date", "company_name", "total_amount"]
                return str(order[keys[col]])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None
