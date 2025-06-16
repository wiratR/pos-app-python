from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QHBoxLayout
)

class EditProductDialog(QDialog):
    def __init__(self, product_id, name, description, price, parent=None):
        super().__init__(parent)
        self.setWindowTitle("อัปเดตข้อมูลสินค้า")
        self.product_id = product_id

        self.name_edit = QLineEdit(name)
        self.desc_edit = QLineEdit(description)
        self.price_edit = QLineEdit(str(price))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("ชื่อ:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("รายละเอียด:"))
        layout.addWidget(self.desc_edit)
        layout.addWidget(QLabel("ราคา:"))
        layout.addWidget(self.price_edit)

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

        # Flag to indicate delete action
        self.delete_requested = False

    def save(self):
        try:
            price = float(self.price_edit.text())
        except ValueError:
            QMessageBox.warning(self, "ข้อมูลผิดพลาด", "ราคาต้องเป็นตัวเลข")
            return

        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "ข้อมูลผิดพลาด", "ชื่อสินค้าห้ามเว้นว่าง")
            return

        self.name = self.name_edit.text().strip()
        self.description = self.desc_edit.text().strip()
        self.price = price
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
