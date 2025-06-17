from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QSpinBox,
    QFormLayout, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from controllers.order_controller import OrderController


class OrderProductDialog(QDialog):
    def __init__(self, products, order_id=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("สั่งซื้อสินค้า")
        self.setFixedWidth(600)
        self.products = products

        layout = QVBoxLayout()

        # Customer Info Fields
        customer_form = QFormLayout()

        self.order_input = QLineEdit()
        self.order_input.setText(order_id or "")
        self.order_input.setReadOnly(True)

        self.order_date_input = QDateEdit(calendarPopup=True)
        self.order_date_input.setDate(QDate.currentDate())

        self.delivery_date_input = QDateEdit(calendarPopup=True)
        self.delivery_date_input.setDate(QDate.currentDate())

        self.company_name_input = QLineEdit()
        self.company_address_input = QLineEdit()
        self.contact_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.tax_id_input = QLineEdit()

        for field in [
            self.order_input, self.order_date_input,
            self.delivery_date_input, self.company_name_input,
            self.company_address_input, self.contact_name_input,
            self.phone_input, self.email_input, self.tax_id_input
        ]:
            field.setFixedWidth(400)

        customer_form.addRow("เลขที่คำสั่งซื้อ:", self.order_input)
        customer_form.addRow("วันที่สั่งซื้อ:", self.order_date_input)
        customer_form.addRow("วันที่ส่งสินค้า:", self.delivery_date_input)
        customer_form.addRow("ชื่อบริษัท:", self.company_name_input)
        customer_form.addRow("เลขที่ภาษี:", self.tax_id_input)
        customer_form.addRow("ที่อย่บริษัท:", self.company_address_input)
        customer_form.addRow("ชื่อผู้ติดต่อ:", self.contact_name_input)
        customer_form.addRow("เบอร์โทรศัพท์:", self.phone_input)
        customer_form.addRow("อีเมล:", self.email_input)

        layout.addLayout(customer_form)

        # Product Table
        self.table = QTableWidget(len(products), 4)
        self.table.setHorizontalHeaderLabels(["สินค้า", "ราคา/ ชิ้น", "จำนวน", "ราคารวม"])

        for row, (name, price) in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{price:.2f}"))

            qty_widget = QWidget()
            qty_layout = QHBoxLayout()
            qty_layout.setContentsMargins(0, 0, 0, 0)
            qty_spin = QSpinBox()
            qty_spin.setRange(0, 999)
            qty_spin.valueChanged.connect(self.update_totals)
            qty_layout.addWidget(qty_spin)
            qty_widget.setLayout(qty_layout)
            self.table.setCellWidget(row, 2, qty_widget)

            self.table.setItem(row, 3, QTableWidgetItem("0.00"))

        self.total_label = QLabel("รวมทั้งสิ้น: 0.00 บาท")

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

        self.confirm_button.clicked.connect(self.confirm_order)
        self.cancel_button.clicked.connect(self.reject)

    def update_totals(self):
        total = 0.0
        for row in range(self.table.rowCount()):
            price = float(self.table.item(row, 1).text())
            qty_spin = self.table.cellWidget(row, 2).findChild(QSpinBox)
            qty = qty_spin.value()
            subtotal = qty * price
            self.table.setItem(row, 3, QTableWidgetItem(f"{subtotal:.2f}"))
            total += subtotal

        self.total_label.setText(f"รวมทั้งสิ้น: {total:.2f} บาท")

    def get_product_id_by_name(self, name):
        for i, (p_name, _) in enumerate(self.products):
            if p_name == name:
                return i + 1  # assuming product_id is index+1
        return None

    def confirm_order(self):
        order_no = self.order_input.text().strip()
        order_date = self.order_date_input.date().toString("dd/MM/yyyy")
        delivery_date = self.delivery_date_input.date().toString("dd/MM/yyyy")
        company = self.company_name_input.text().strip()
        tax_id = self.tax_id_input.text().strip()
        address = self.company_address_input.text().strip()
        name = self.contact_name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if not all([company, tax_id, address, name, phone, email]):
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกข้อมูลลูกค้าให้ครบถ้วน รวมถึง Tax ID")
            return

        items = []
        for row in range(self.table.rowCount()):
            qty_spin = self.table.cellWidget(row, 2).findChild(QSpinBox)
            qty = qty_spin.value()
            if qty > 0:
                product_name = self.table.item(row, 0).text()
                product_id = self.get_product_id_by_name(product_name)
                subtotal = float(self.table.item(row, 3).text())
                items.append((product_id, qty, subtotal))

        if not items:
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณาเลือกสินค้าอย่างน้อยหนึ่งรายการ")
            return

        controller = OrderController()
        total_amount = float(self.total_label.text().split(":")[1].replace("บาท", "").strip())

        order_data = {
            'order_no': order_no,
            'order_date': QDate.fromString(order_date, "dd/MM/yyyy").toString("yyyy-MM-dd"),
            'delivery_date': QDate.fromString(delivery_date, "dd/MM/yyyy").toString("yyyy-MM-dd"),
            'company_name': company,
            'company_address': address,
            'contact_name': name,
            'phone': phone,
            'email': email,
            'tax_id': tax_id,
            'total_amount': total_amount
        }

        controller.create_order(order_data, items)

        QMessageBox.information(
            self,
            "สั่งซื้อสำเร็จ",
            f"เลขที่คำสั่งซื้อ: {order_no}\n"
            f"วันที่สั่งซื้อ: {order_date}\n"
            f"วันที่ส่งสินค้า: {delivery_date}\n\n"
            f"บริษัท: {company}\n"
            f"เลขที่ภาษี: {tax_id}\n"
            f"ที่อยู่: {address}\n"
            f"ชื่อผู้ติดต่อ: {name}\n"
            f"โทร: {phone}, อีเมล: {email}\n\n"
            f"คำสั่งซื้อสำเร็จแล้ว"
        )
        self.accept()
