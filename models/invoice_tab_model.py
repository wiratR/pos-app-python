from PyQt6.QtCore import QAbstractTableModel, Qt

class InvoiceTableModel(QAbstractTableModel):
    def __init__(self, order_model):
        super().__init__()
        self.order_model = order_model
        self.orders = self.order_model.get_paid_orders()

    def rowCount(self, parent=None):
        return len(self.orders)

    def columnCount(self, parent=None):
        return 7  # เพิ่มคอลัมน์ที่ 6 สำหรับปุ่ม "ใบกำกับภาษี"

    def headerData(self, section, orientation, role):
        headers = ["เลขที่", "วันที่สั่งซื้อ", "วันที่ส่ง", "วันที่ชำระเงิน", "บริษัท", "รวมเงิน", "ใบกำกับภาษี"]
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return headers[section]
        return None
    
    def refresh_data(self):
        new_orders = self.order_model.get_paid_orders()
        self.beginResetModel()
        self.orders = new_orders
        self.endResetModel()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        row = index.row()
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col < 6:
                return str(self.orders[row][col])
            elif col == 6:
                return "พิมพ์"  # ให้แสดงข้อความใน cell ปุ่ม
        return None