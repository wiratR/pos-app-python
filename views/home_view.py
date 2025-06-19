import os
import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QGroupBox, QSpinBox,
    QLineEdit, QPushButton, QMessageBox, QCalendarWidget, QTableView
)
from PyQt6.QtCore import QTimer, QModelIndex
from PyQt6.uic import loadUi

from delegates.button_delegate import ModernButtonDelegate  
from models.product_model import ProductModel
from models.product_table_model import ProductTableModel
from views.add_product_dialog import AddProductDialog
from views.edit_product_dialog import EditProductDialog
from views.order_product_dialog import OrderProductDialog 
from controllers.order_controller import OrderController
from models.order_table_model import OrderTableModel  # ⬅️ new model
from views.pdf_viewer import PDFViewer  # ⬅️ new PDF viewer
from utils.path_utils import resource_path
from utils.generate_delivery_pdf import generate_delivery_pdf
from utils.generate_quotation_pdf import generate_quotation_pdf  # ⬅️ new PDF generation utility

class HomeView(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file = resource_path(os.path.join("resources", "ui", "home_view.ui"))
        loadUi(ui_file, self)
        logging.info("🔧 Loading HomeView UI from %s", ui_file)

        self.showFullScreen()  # 👈 This line enables full-screen view

        self.orderController = OrderController()  # ⬅️ initialize controller

        # === Widgets ===
        self.datetimeLabel: QLabel = self.findChild(QLabel, "datetimeLabel")
        self.spinBox: QSpinBox = self.findChild(QSpinBox, "spinBox")
        self.lineEdit: QLineEdit = self.findChild(QLineEdit, "lineEdit")
        self.calculateButton: QPushButton = self.findChild(QPushButton, "pushButton_4")
        self.calculateButton.clicked.connect(self.calculate_cost)

        self.reportButton: QPushButton = self.findChild(QPushButton, "pushButton")
        self.reportButton.clicked.connect(self.show_report)

        self.calendar_start: QCalendarWidget = self.findChild(QCalendarWidget, "calendarWidget")
        self.calendar_end: QCalendarWidget = self.findChild(QCalendarWidget, "calendarWidget_2")

        self.groupBoxRight: QGroupBox = self.findChild(QGroupBox, "groupBoxRight")
        self.groupBoxRight.setFixedWidth(350)

        # # === Product Table ===
        # --- Product TableView & Model setup ---
        self.tableView: QTableView = self.findChild(QTableView, "tableView_2")

        # Initialize the data-model (ProductModel → SQLite) and the Qt-table-model
        # Setup product model with DB path
        db_path = resource_path(os.path.join("database", "app.sqlite"))
        product_data_model = ProductModel(db_path=db_path)

        # Setup table model for Qt view
        table_model = ProductTableModel(product_data_model)
        self.tableView.setModel(table_model)

        self.tableView.resizeColumnsToContents()

        # Connect double-click signal to the edit method
        self.tableView.doubleClicked.connect(self.on_table_double_click)

        # Add product button
        self.addButton: QPushButton = self.findChild(QPushButton, "addButton")
        self.addButton.clicked.connect(self.add_product)

        # Load product names for order dialog
        self.pushButtonOrder.clicked.connect(self.open_order_dialog)

        # === Order TableView for tab ใบส่งของ ===
        self.orderTableView: QTableView = self.findChild(QTableView, "tableView")  # This is from tab2
        self.load_order_data()

        # ใช้ ModernButtonDelegate สำหรับใบส่งของ ใบส่งของ - ปุ่มสีฟ้า
        delivery_delegate = ModernButtonDelegate(self.orderTableView, label="📄 ใบส่งของ", color="#2196F3")
        delivery_delegate.button_signal.clicked.connect(self.on_delivery_note_clicked)
        self.orderTableView.setItemDelegateForColumn(5, delivery_delegate)

        # ใช้ ModernButtonDelegate สำหรับใบเสนอราคา ใบเสนอราคา - ปุ่มสีส้ม
        quotation_delegate = ModernButtonDelegate(self.orderTableView, label="📑 ใบเสนอราคา", color="#FF9800")
        quotation_delegate.button_signal.clicked.connect(self.on_quotation_clicked)
        self.orderTableView.setItemDelegateForColumn(6, quotation_delegate)

        # ขนาดของแถว
        self.orderTableView.verticalHeader().setDefaultSectionSize(40)
        self.orderTableView.resizeColumnsToContents()  # ปรับขนาดคอลัมน์อื่นก่อน
        self.orderTableView.setColumnWidth(5, 140)     # ตั้งขนาดคอลัมน์ปุ่มใหม่
        self.orderTableView.setColumnWidth(6, 140)

        # === Clock update ===
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

        self.statusBar().addPermanentWidget(self.datetimeLabel)

        logging.info("✅ HomeView loaded successfully")

    def update_datetime(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.datetimeLabel.setText(now)
        logging.debug(f"⏰ Updated datetime: {now}")

    def calculate_cost(self):
        try:
            qty = self.spinBox.value()
            price = float(self.lineEdit.text())
            total = qty * price
            QMessageBox.information(self, "ผลลัพธ์", f"ต้นทุนรวม: {total:.2f} บาท")
            logging.info(f"✅ Calculated total: {total:.2f}")
        except ValueError:
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกราคาขายให้ถูกต้อง")
            logging.warning("❌ Invalid input for price.")

    def show_report(self):
        start_date = self.calendar_start.selectedDate().toString("yyyy-MM-dd")
        end_date = self.calendar_end.selectedDate().toString("yyyy-MM-dd")
        QMessageBox.information(self, "ออกรายงาน", f"ออกรายงานระหว่างวันที่ {start_date} ถึง {end_date}")
        logging.info(f"📄 Generate report from {start_date} to {end_date}")
    
    def on_table_double_click(self, index: QModelIndex):
        if not index.isValid():
            return

        row = index.row()
        model = self.tableView.model()

        # Retrieve current product data from the model
        product_id = model.get_product_id(row)
        name = model.data(model.index(row, 0))
        description = model.data(model.index(row, 1))
        price = model.data(model.index(row, 2))

        # Open the edit dialog
        dialog = EditProductDialog(product_id, name, description, float(price), self)
        
        if dialog.exec():
            if dialog.delete_requested:
                # User confirmed delete
                confirm = QMessageBox.question(
                    self,
                    "ยืนยันการลบ",
                    f"คุณแน่ใจว่าต้องการลบสินค้าชื่อ \"{name}\"?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if confirm == QMessageBox.StandardButton.Yes:
                    model.delete_product(product_id)
            else:
                # User saved changes
                model.update_product(
                    product_id,
                    dialog.name,
                    dialog.description,
                    dialog.price
                )
            # Refresh the view
            model.layoutChanged.emit()

    def add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec():
            name, description, price = dialog.get_data()

            # Add to DB and refresh table
            model = self.tableView.model()
            model.product_model.add_product(name, description, price)
            model._products = model.product_model.get_all_products()
            model.layoutChanged.emit()

            QMessageBox.information(self, "เพิ่มสินค้า", "เพิ่มสินค้าเรียบร้อยแล้ว")

    def load_product_names(self):
        model = self.tableView.model()
        products = []
        for row in range(model.rowCount()):
            # assuming product name is in column 0
            index = model.index(row, 0)
            product_name = model.data(index)
            products.append(product_name)
        return products

    def open_order_dialog(self):
        order_id = self.lineEditOrderId.text().strip()
        if not order_id:
            QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณากรอกเลขที่คำสั่งซื้อก่อนทำรายการ")
            return

        product_list = self.tableView.model().get_product_list_for_order()
        dialog = OrderProductDialog(product_list, order_id, self)
        if dialog.exec():
            # Optionally handle the confirmed order here
            pass

    def load_order_data(self):
        orders = self.orderController.get_all_orders()
        table_model = OrderTableModel(orders)
        self.orderTableView.setModel(table_model)
        self.orderTableView.resizeColumnsToContents()

    def on_delivery_note_clicked(self, row: int):
        logging.info(f"🧾 เริ่มสร้างใบส่งของจากแถวที่: {row}")

        model = self.orderTableView.model()
        order = model.orders[row]

        items = [
            {"product": "สินค้า A", "qty": 2, "price": 50.0},
            {"product": "สินค้า B", "qty": 1, "price": 100.0}
        ]

        try:
            os.makedirs("output", exist_ok=True)
            order_no = order.get("order_no", f"no-id-{datetime.now().timestamp()}")
            # use resource_path
            output_dir = os.path.abspath("output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"ใบส่งของ_{order_no}.pdf")
            # output_path = os.path.join("output", f"ใบส่งของ_{order_no}.pdf")
            logging.info(f"📄 สร้างไฟล์ PDF ที่: {output_path}")

            generate_delivery_pdf(order, items, output_path)

            logging.info("✅ สร้างใบส่งของ PDF เสร็จสมบูรณ์")

            self.pdf_viewer = PDFViewer(output_path)
            self.pdf_viewer.show()

        except Exception as e:
            logging.error(f"❌ เกิดข้อผิดพลาดขณะสร้างใบส่งของ: {e}", exc_info=True)
            QMessageBox.critical(self, "ผิดพลาด", f"ไม่สามารถสร้างใบส่งของได้: {e}")

    def on_quotation_clicked(self, row):
        logging.info(f"📑 สร้างใบเสนอราคา สำหรับแถว {row}")
        model = self.orderTableView.model()
        order = model.orders[row]

        items = [
            {"name": "สินค้า A", "quantity": 2, "unit_price": 50.0},
            {"name": "สินค้า B", "quantity": 1, "unit_price": 100.0}
        ]

        try:
            os.makedirs("output", exist_ok=True)
            order_no = order.get("order_no", f"no-id-{datetime.now().timestamp()}")
            output_dir = os.path.abspath("output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"ใบเสนอราคา_{order_no}.pdf")
            logging.info(f"📄 สร้างไฟล์ PDF ที่: {output_path}")

            generate_quotation_pdf(order, items, output_path)

            logging.info("✅ สร้างใบเสนอราคา PDF เสร็จสมบูรณ์")

            self.pdf_viewer = PDFViewer(output_path)
            self.pdf_viewer.show()
        
        except Exception as e:
            logging.error(f"❌ เกิดข้อผิดพลาดขณะสร้างใบเสนอราคา: {e}", exc_info=True)
            QMessageBox.critical(self, "ผิดพลาด", f"ไม่สามารถสร้างใบเสนอราคาได้: {e}")