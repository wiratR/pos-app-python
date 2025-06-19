from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QIntValidator

class EditProductDialog(QDialog):
    def __init__(self, product_id, name, description, price, stock_quantity, parent=None):
        super().__init__(parent)
        self.setWindowTitle("อัปเดตข้อมูลสินค้า")
        self.product_id = product_id

        self.name_edit = QLineEdit(name)
        self.desc_edit = QLineEdit(description)
        self.price_edit = QLineEdit(str(price))
        self.stock_edit = QLineEdit(str(stock_quantity))
        self.stock_edit.setValidator(QIntValidator(0, 999999))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("ชื่อสินค้า:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("รายละเอียดสินค้า:"))
        layout.addWidget(self.desc_edit)
        layout.addWidget(QLabel("ราคาขาย:"))
        layout.addWidget(self.price_edit)
        layout.addWidget(QLabel("จำนวนสต็อก:"))
        layout.addWidget(self.stock_edit)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("บันทึก")
        self.delete_btn = QPushButton("ลบ")
        self.cancel_btn = QPushButton("ยกเลิก")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.save_btn.clicked.connect(self.save)
        self.delete_btn.clicked.connect(self.confirm_delete)
        self.cancel_btn.clicked.connect(self.reject)

        # Flags
        self.delete_requested = False
        self.name = ""
        self.description = ""
        self.price = 0.0
        self.stock_quantity = 0

    def save(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "ข้อมูลผิดพลาด", "ชื่อสินค้าห้ามเว้นว่าง")
            return
        try:
            price = float(self.price_edit.text())
        except ValueError:
            QMessageBox.warning(self, "ข้อมูลผิดพลาด", "ราคาต้องเป็นตัวเลข")
            return
        try:
            stock_qty = int(self.stock_edit.text())
        except ValueError:
            QMessageBox.warning(self, "ข้อมูลผิดพลาด", "จำนวนสต็อกต้องเป็นตัวเลขจำนวนเต็ม")
            return

        self.name = self.name_edit.text().strip()
        self.description = self.desc_edit.text().strip()
        self.price = price
        self.stock_quantity = stock_qty
        self.accept()

    def confirm_delete(self):
        reply = QMessageBox.question(
            self,
            "ยืนยันการลบ",
            "คุณต้องการลบสินค้านี้ใช่หรือไม่?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.delete_requested = True
            self.accept()

    def get_updated_data(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock_quantity": self.stock_quantity
        }
