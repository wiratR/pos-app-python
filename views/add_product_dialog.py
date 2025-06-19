from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QPushButton
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("เพิ่มสินค้า")

        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()

        self.price_input = QLineEdit()
        self.price_input.setValidator(QDoubleValidator(0.00, 9999999.99, 2))

        self.cost_price_input = QLineEdit()
        self.cost_price_input.setValidator(QDoubleValidator(0.00, 9999999.99, 2))

        self.stock_qty_input = QLineEdit()
        self.stock_qty_input.setValidator(QIntValidator(0, 999999))

        form_layout = QFormLayout()
        form_layout.addRow("ชื่อสินค้า:", self.name_input)
        form_layout.addRow("รายละเอียดสินค้า:", self.desc_input)
        form_layout.addRow("ราคาขายสินค้า:", self.price_input)
        form_layout.addRow("ราคาต้นทุน:", self.cost_price_input)
        form_layout.addRow("จำนวนสต็อก:", self.stock_qty_input)

        # Create custom buttons
        self.save_button = QPushButton("บันทึก")
        self.cancel_button = QPushButton("ยกเลิก")

        # Button box layout
        self.buttons = QDialogButtonBox()
        self.buttons.addButton(self.save_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttons.addButton(self.cancel_button, QDialogButtonBox.ButtonRole.RejectRole)

        # Connect buttons to accept/reject
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.buttons)

        self.setLayout(main_layout)

    def accept(self) -> None:
        # Validate inputs
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกชื่อสินค้า")
            return
        if not self.price_input.text().strip():
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกราคาขายสินค้า")
            return
        if not self.cost_price_input.text().strip():
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกราคาต้นทุน")
            return
        if not self.stock_qty_input.text().strip():
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกจำนวนสต็อก")
            return

        try:
            price = float(self.price_input.text())
            cost_price = float(self.cost_price_input.text())
            stock_qty = int(self.stock_qty_input.text())
        except ValueError:
            QMessageBox.warning(self, "ข้อผิดพลาด", "ราคาสินค้าและจำนวนสต็อกต้องเป็นตัวเลขที่ถูกต้อง")
            return

        if cost_price > price:
            QMessageBox.warning(self, "ข้อผิดพลาด", "ราคาต้นทุนไม่ควรมากกว่าราคาขาย")
            return

        if stock_qty < 0:
            QMessageBox.warning(self, "ข้อผิดพลาด", "จำนวนสต็อกต้องไม่ติดลบ")
            return

        super().accept()

    def get_data(self):
        return {
            'name': self.name_input.text().strip(),
            'description': self.desc_input.text().strip(),
            'price': float(self.price_input.text().strip()),
            'cost_price': float(self.cost_price_input.text().strip()),
            'stock_quantity': int(self.stock_qty_input.text().strip())
        }
