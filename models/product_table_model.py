from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from typing import List

class ProductTableModel(QAbstractTableModel):
    def __init__(self, product_model, parent=None):
        super().__init__(parent)
        self.product_model = product_model
        self.headers = ["ชื่อสินค้า", "รายละเอียด", "ราคา"]
        self._products = self.product_model.get_all_products()  # fetch data once

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._products)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        product = self._products[index.row()]
        column = index.column()

        if column == 0:
            return product["name"]
        elif column == 1:
            return product["description"]
        elif column == 2:
            return f"{product['price']:.2f}"

        return QVariant()

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return QVariant()

        if orientation == Qt.Orientation.Horizontal and section < len(self.headers):
            return self.headers[section]

        return QVariant()

    def get_product_id(self, row: int) -> int:
        return self._products[row]["id"]

    def update_product(self, product_id: int, name: str, description: str, price: float):
        self.product_model.update_product(product_id, name, description, price)
        self._products = self.product_model.get_all_products()  # refresh data
        self.layoutChanged.emit()
    
    def delete_product(self, product_id: int):
        success = self.product_model.delete_product(product_id)
        if success:
            self._products = self.product_model.get_all_products()
            self.layoutChanged.emit()  # Refresh the table after deletion
        return success