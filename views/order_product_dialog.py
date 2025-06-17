from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QSpinBox,
    QFormLayout, QDateEdit
)
from PyQt6.QtCore import Qt, QDate


class OrderProductDialog(QDialog):
    def __init__(self, products, order_id=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("สั่งซื้อสินค้า")
        self.setFixedWidth(600)  # ✅ Set fixed width
        self.products = products

        layout = QVBoxLayout()

        # === Customer Info Fields ===
        customer_form = QFormLayout()

        self.order_input = QLineEdit()
        self.order_input.setText(order_id or "")
        self.order_input.setReadOnly(True)

        self.order_date_input = QDateEdit()
        self.order_date_input.setCalendarPopup(True)
        self.order_date_input.setDate(QDate.currentDate())

        self.delivery_date_input = QDateEdit()
        self.delivery_date_input.setCalendarPopup(True)
        self.delivery_date_input.setDate(QDate.currentDate())

        self.company_name_input = QLineEdit()
        self.company_address_input = QLineEdit()
        self.contact_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        # Optional: set fixed width to inputs
        for field in [
            self.order_input, self.order_date_input, 
            self.delivery_date_input, self.company_name_input, 
            self.company_address_input, self.contact_name_input, 
            self.phone_input, self.email_input
        ]:
            field.setFixedWidth(400)

        customer_form.addRow("เลขที่คำสั่งซื้อ:", self.order_input)
        customer_form.addRow("วันที่สั่งซื้อ:", self.order_date_input)
        customer_form.addRow("วันที่ส่งสินค้า:", self.delivery_date_input)
        customer_form.addRow("ชื่อบริษัท:", self.company_name_input)
        customer_form.addRow("ที่อยู่บริษัท:", self.company_address_input)
        customer_form.addRow("ชื่อผู้ติดต่อ:", self.contact_name_input)
        customer_form.addRow("เบอร์โทรศัพท์:", self.phone_input)
        customer_form.addRow("อีเมล:", self.email_input)

        layout.addLayout(customer_form)

        # === Product Table ===
        self.table = QTableWidget(len(products), 4)
        self.table.setHorizontalHeaderLabels(["สินค้า", "ราคา/ชิ้น", "จำนวน", "ราคารวม"])
        self.table.setColumnWidth(0, 180)  # สินค้า
        self.table.setColumnWidth(1, 100)  # ราคา
        self.table.setColumnWidth(2, 80)   # จำนวน
        self.table.setColumnWidth(3, 100)  # รวม

        for row, (name, price) in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{price:.2f}"))

            qty_widget = QWidget()
            qty_layout = QHBoxLayout()
            qty_layout.setContentsMargins(0, 0, 0, 0)
            qty_spin = QSpinBox()
            qty_spin.setValue(0)
            qty_spin.setMinimum(0)
            qty_spin.setMaximum(999)
            qty_spin.valueChanged.connect(self.update_totals)
            qty_layout.addWidget(qty_spin)
            qty_widget.setLayout(qty_layout)
            self.table.setCellWidget(row, 2, qty_widget)

            self.table.setItem(row, 3, QTableWidgetItem("0.00"))

        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 120)

        self.total_label = QLabel("รวมทั้งสิ้น: 0.00 บาท")

        # Buttons
        button_layout = QHBoxLayout()
        self.confirm_button = QPushButton("ยืนยัน")
        self.cancel_button = QPushButton("ยกเลิก")
        button_layout.addWidget(self.confirm_button)
        button_layout.addWidget(self.cancel_button)

        layout.addWidget(QLabel("เลือกรายการสินค้า:"))
        layout.addWidget(self.table)
        layout.addWidget(self.total_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connect
        self.confirm_button.clicked.connect(self.confirm_order)
        self.cancel_button.clicked.connect(self.reject)

    def update_totals(self):
        total = 0.0
        for row in range(self.table.rowCount()):
            price_item = self.table.item(row, 1)
            price = float(price_item.text()) if price_item else 0.0

            qty_widget = self.table.cellWidget(row, 2)
            qty_spin = qty_widget.findChild(QSpinBox)
            qty = qty_spin.value() if qty_spin else 0

            subtotal = qty * price
            self.table.setItem(row, 3, QTableWidgetItem(f"{subtotal:.2f}"))
            total += subtotal

        self.total_label.setText(f"รวมทั้งสิ้น: {total:.2f} บาท")

    def confirm_order(self):
        order_no = self.order_input.text().strip()
        order_date = self.order_date_input.date().toString("dd/MM/yyyy")
        delivery_date = self.delivery_date_input.date().toString("dd/MM/yyyy")
        company = self.company_name_input.text().strip()
        address = self.company_address_input.text().strip()
        name = self.contact_name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not all([company, address, name, phone, email]):
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกข้อมูลลูกค้าให้ครบถ้วน")
            return

        ordered_items = []
        for row in range(self.table.rowCount()):
            qty_widget = self.table.cellWidget(row, 2)
            qty_spin = qty_widget.findChild(QSpinBox)
            qty = qty_spin.value()
            if qty > 0:
                product_name = self.table.item(row, 0).text()
                subtotal = self.table.item(row, 3).text()
                ordered_items.append(f"{product_name} × {qty} = {subtotal} บาท")

        if not ordered_items:
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณาเลือกสินค้าอย่างน้อยหนึ่งรายการ")
            return

        QMessageBox.information(
            self,
            "สั่งซื้อสำเร็จ",
            f"เลขที่คำสั่งซื้อ: {order_no}\n"
            f"วันที่สั่งซื้อ: {order_date}\n"
            f"วันที่ส่งสินค้า: {delivery_date}\n\n"
            f"บริษัท: {company}\n"
            f"ที่อยู่: {address}\n"
            f"ชื่อผู้ติดต่อ: {name}\n"
            f"โทร: {phone}, อีเมล: {email}\n\n"
            f"รายการสินค้า:\n" + "\n".join(ordered_items)
        )
        self.accept()
