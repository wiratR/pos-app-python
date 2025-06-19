# from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant

# class OrderTableModel(QAbstractTableModel):
#     def __init__(self, orders):
#         super().__init__()
#         self.orders = orders
#         self.headers = ["เลขที่ใบสั่ง", "วันที่สั่ง", "วันที่ส่ง", "ชื่อลูกค้า", "ยอดรวม", ""]  # empty header for button

#     def rowCount(self, parent=None):
#         return len(self.orders)

#     def columnCount(self, parent=None):
#         return len(self.headers)

#     def data(self, index, role):
#         if not index.isValid():
#             return None

#         if role == Qt.ItemDataRole.DisplayRole:
#             if index.column() == 5:  # Button column
#                 return "ใบส่งของ"
#             order = self.orders[index.row()]
#             keys = ["order_no", "order_date", "delivery_date", "company_name", "total_amount"]
#             return str(order[keys[index.column()]])
#         return None

#     def headerData(self, section, orientation, role):
#         if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
#             return self.headers[section]
#         return None

from PyQt6.QtCore import QAbstractTableModel, Qt

class OrderTableModel(QAbstractTableModel):
    def __init__(self, orders):
        super().__init__()
        self.orders = orders
        # เพิ่มหัวข้อ "ใบเสนอราคา"
        self.headers = ["เลขที่ใบสั่ง", "วันที่สั่ง", "วันที่ส่ง", "ชื่อลูกค้า", "ยอดรวม", "ใบส่งของ", "ใบเสนอราคา"]

    def rowCount(self, parent=None):
        return len(self.orders)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            col = index.column()
            if col == 5:
                return "ใบส่งของ"
            elif col == 6:
                return "ใบเสนอราคา"
            else:
                order = self.orders[index.row()]
                keys = ["order_no", "order_date", "delivery_date", "company_name", "total_amount"]
                return str(order[keys[col]])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None
