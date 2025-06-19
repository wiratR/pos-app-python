from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QPushButton

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("เพิ่มสินค้า")

        self.name_input = QLineEdit()
        self.desc_input = QLineEdit()
        self.price_input = QLineEdit()

        form_layout = QFormLayout()
        form_layout.addRow("ชื่อสินค้า:", self.name_input)
        form_layout.addRow("รายละเอียดสินค้า:", self.desc_input)
        form_layout.addRow("ราคาสินค้า:", self.price_input)

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
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกราคาสินค้า")
            return
        try:
            float(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, "ข้อผิดพลาด", "ราคาสินค้าต้องเป็นตัวเลข")
            return
        super().accept()

    def get_data(self):
        return (
            self.name_input.text().strip(),
            self.desc_input.text().strip(),
            float(self.price_input.text().strip())
        )
    
