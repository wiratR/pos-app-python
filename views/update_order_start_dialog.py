from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QMessageBox

class UpdateOrderStatusDialog(QDialog):
    def __init__(self, current_status, parent=None):
        super().__init__(parent)
        self.setWindowTitle("แก้ไขสถานะคำสั่งซื้อ")
        self.resize(300, 100)
        layout = QVBoxLayout()

        self.status_map = {
            "รอดำเนินการ": "pending",
            "ชำระเงินแล้ว": "paid",
            "ยังไม่ชำระ": "unpaid",
            "ยกเลิก": "cancelled",
        }

        layout.addWidget(QLabel("เลือกสถานะคำสั่งซื้อ:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(self.status_map.keys())

        # หา key ที่ตรงกับค่า current_status เพื่อ set ให้ตรง
        key_for_status = next((k for k,v in self.status_map.items() if v == current_status), None)
        if key_for_status:
            self.status_combo.setCurrentText(key_for_status)
        else:
            self.status_combo.setCurrentIndex(0)

        layout.addWidget(self.status_combo)

        self.btn_confirm = QPushButton("บันทึก")
        layout.addWidget(self.btn_confirm)

        self.setLayout(layout)

        self.btn_confirm.clicked.connect(self.accept)

    def get_selected_status(self):
        # แปลงกลับเป็นค่าที่เก็บฐานข้อมูล
        selected_key = self.status_combo.currentText()
        return self.status_map.get(selected_key, "pending")
