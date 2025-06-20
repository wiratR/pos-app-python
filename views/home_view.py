import os
import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QGroupBox, QSpinBox,
    QLineEdit, QPushButton, QMessageBox, QCalendarWidget, QTableView, QTabWidget
)
from PyQt6.QtCore import QTimer, QModelIndex
from PyQt6.uic import loadUi

# Importing necessary modules and classes
from utils.generate_invoice_pdf import generate_invoice_pdf
from utils.path_utils import resource_path
from utils.generate_delivery_pdf import generate_delivery_pdf
from utils.generate_quotation_pdf import generate_quotation_pdf
from delegates.button_delegate import ModernButtonDelegate  
from views.add_product_dialog import AddProductDialog
from views.edit_product_dialog import EditProductDialog
from views.order_product_dialog import OrderProductDialog 
from views.update_order_start_dialog import UpdateOrderStatusDialog  # ⬅️ new PDF generation utility
from views.pdf_viewer import PDFViewer  # ⬅️ new PDF viewer
from controllers.product_controller import ProductController
from controllers.order_controller import OrderController
from controllers.stock_controller import StockController
from models.product_table_model import ProductTableModel 
from models.product_model import ProductModel 
from models.order_table_model import OrderTableModel  # ⬅️ new model
from models.invoice_tab_model import InvoiceTableModel  # ⬅️ new invoice model

class HomeView(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file = resource_path(os.path.join("resources", "ui", "home_view.ui"))
        loadUi(ui_file, self)
        logging.info("🔧 Loading HomeView UI from %s", ui_file)

        self.showFullScreen()  # 👈 This line enables full-screen view

        self.orderController = OrderController()  # ⬅️ initialize controller
        self.productController = ProductController()  # ⬅️ initialize product controller
        self.stockController = StockController()  # ⬅️ initialize stock controller

        # === Widgets ===
        self.datetimeLabel: QLabel = self.findChild(QLabel, "datetimeLabel")
        self.spinBox: QSpinBox = self.findChild(QSpinBox, "spinBox")
        self.lineEdit: QLineEdit = self.findChild(QLineEdit, "lineEdit")
        self.pushButton_calculate_cost = self.findChild(QPushButton, "pushButton_calculate_cost")
        self.pushButton_calculate_cost.clicked.connect(self.calculate_cost)

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
        self.orderTableView.setItemDelegateForColumn(6, delivery_delegate)

        # ใช้ ModernButtonDelegate สำหรับใบเสนอราคา ใบเสนอราคา - ปุ่มสีส้ม
        quotation_delegate = ModernButtonDelegate(self.orderTableView, label="📑 ใบเสนอราคา", color="#FF9800")
        quotation_delegate.button_signal.clicked.connect(self.on_quotation_clicked)
        self.orderTableView.setItemDelegateForColumn(7, quotation_delegate)

        self.orderTableView.clicked.connect(self.on_order_table_clicked)

        # ขนาดของแถว
        self.orderTableView.verticalHeader().setDefaultSectionSize(40)
        self.orderTableView.resizeColumnsToContents()  # ปรับขนาดคอลัมน์อื่นก่อน
        self.orderTableView.setColumnWidth(5, 140)     # ตั้งขนาดคอลัมน์ปุ่มใหม่
        self.orderTableView.setColumnWidth(6, 140)     # ตั้งขนาดคอลัมน์ปุ่มใหม่
        self.orderTableView.setColumnWidth(7, 140)

        order_model =  self.orderController
        # สร้างโมเดลตารางใบแจ้งหนี้
        self.invoice_model = InvoiceTableModel(order_model)
        self.tableView_invoices.setModel(self.invoice_model)
        self.tableView_invoices.resizeColumnsToContents()  # ปรับขนาดคอลัมน์อื่นก่อน
        self.tableView_invoices.setColumnWidth(6, 140)     # ตั้งขนาดคอลัมน์ปุ่มใหม่

        # Delegate
        invoice_delegate = ModernButtonDelegate(self.tableView_invoices, label="📑 ใบเสร็จรับเงิน", color="#4CAF50")
        invoice_delegate.button_signal.clicked.connect(self.on_invoice_button_clicked)
        self.tableView_invoices.setItemDelegateForColumn(6, invoice_delegate)

        # TabWidget control
        self.tabWidget = self.findChild(QTabWidget, "tabWidget")  # ใช้ชื่อ object ใน .ui
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

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

        # ดึงข้อมูลสินค้า
        product_id = model.get_product_id(row)
        name = model.data(model.index(row, 0))
        description = model.data(model.index(row, 1))
        price = model.data(model.index(row, 2))

        # ดึง stock_quantity จาก StockModel
        stock_controller = StockController()
        stock_info = stock_controller.get_stock_by_product(product_id)
        stock_quantity = stock_info["stock_quantity"] if stock_info else 0

        # เปิด dialog พร้อม stock_quantity
        dialog = EditProductDialog(product_id, name, description, float(price), stock_quantity, self)

        if dialog.exec():
            if dialog.delete_requested:
                confirm = QMessageBox.question(
                    self,
                    "ยืนยันการลบ",
                    f"คุณแน่ใจว่าต้องการลบสินค้าชื่อ \"{name}\"?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if confirm == QMessageBox.StandardButton.Yes:
                    model.delete_product(product_id)
                    stock_controller.delete_stock(product_id)
            else:
                updated = dialog.get_updated_data()

                # อัปเดตข้อมูลใน ProductModel
                model.update_product(
                    product_id,
                    updated["name"],
                    updated["description"],
                    updated["price"]
                )

                # อัปเดตข้อมูลสต็อกใน StockModel
                stock_controller.update_stock(
                    product_id,
                    quantity=updated["stock_quantity"]
                )

            # Refresh ตาราง
            model._products = model.product_model.get_all_products()
            model.layoutChanged.emit()

    def add_product(self):
        dialog = AddProductDialog(self)
        if dialog.exec():
            data = dialog.get_data()

            name = data['name']
            description = data['description']
            price = data['price']
            cost_price = data['cost_price']
            stock_quantity = data['stock_quantity']

            # Add product to database
            model = self.tableView.model()
            model.product_model.add_product(name, description, price)

            # Get the new product_id (based on name)
            product_id = model.product_model.get_product_id_by_name(name)
            if product_id:
                # Add or update stock entry
                from controllers.stock_controller import StockController
                stock_controller = StockController()
                stock_controller.add_or_update_stock(product_id, stock_quantity, cost_price)

            # Refresh product table
            model._products = model.product_model.get_all_products()
            model.layoutChanged.emit()

            QMessageBox.information(self, "เพิ่มสินค้า", "เพิ่มสินค้าและสต็อกเรียบร้อยแล้ว")


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
            # รีเฟรชตารางออเดอร์เมื่อกด confirm แล้วปิด dialog
            self.load_order_data()

    def load_order_data(self):
        orders = self.orderController.get_all_orders()
        table_model = OrderTableModel(orders)
        self.orderTableView.setModel(table_model)
        self.orderTableView.resizeColumnsToContents()  # ปรับขนาดคอลัมน์อื่นก่อน
        self.orderTableView.setColumnWidth(5, 140)     # ตั้งขนาดคอลัมน์ปุ่มใหม่
        self.orderTableView.setColumnWidth(6, 140)     # ตั้งขนาดคอลัมน์ปุ่มใหม่
        self.orderTableView.setColumnWidth(7, 140)

    def on_delivery_note_clicked(self, row: int):
        logging.info(f"🧾 เริ่มสร้างใบส่งของจากแถวที่: {row}")
        model = self.orderTableView.model()
        order = model.orders[row]
        order_no = order.get("order_no", f"no-id-{datetime.now().timestamp()}")
        logging.info(f"เลขที่คำสั่งซื้อ: {order_no}")
        try:
            # ดึงรายการสินค้าแบบ dynamic จาก DB
            raw_items = self.orderController.get_order_items(order_no)
            logging.info(f"ดึงรายการสินค้า {len(raw_items)} รายการ จาก order_no: {order_no}")

            # ลอง debug ดูรูปแบบข้อมูล
            for item in raw_items:
                logging.debug(f"Raw item: {item} (type: {type(item)})")

            items = []
            for row in raw_items:
                try:
                    # ใช้ชื่อสินค้าใน dict เลย
                    product_name = row['name']
                    qty = int(row['quantity'])
                    unit_price = float(row['unit_price'])

                    items.append({
                        "product": product_name,
                        "qty": qty,
                        "price": unit_price
                    })
                except (ValueError, KeyError, TypeError) as e:
                    logging.warning(f"ข้ามแถวข้อมูลไม่ถูกต้อง: {row} เนื่องจาก: {e}")

            os.makedirs("output", exist_ok=True)
            output_dir = os.path.abspath("output")
            output_path = os.path.join(output_dir, f"ใบส่งของ_{order_no}.pdf")
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
        # ดึง order_no จาก model ของตาราง
        order_no = model.orders[row]['order_no']
        # ดึงรายละเอียดคำสั่งซื้อพร้อมรายการสินค้า
        order = self.orderController.get_order_by_no(order_no)
        items = order.get('items', [])  # ดึงรายการสินค้า

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
    
    def on_invoice_button_clicked(self, row):
        # ดึง order_no จาก model ของตาราง (แก้ตามโครงสร้างของคุณ)
        order_no = self.invoice_model.orders[row][0]  # สมมติ order_no อยู่ index 0
        
        # ดึงรายละเอียดคำสั่งซื้อพร้อม items
        order = self.orderController.get_order_by_no(order_no)
        items = order.get('items', [])  # ดึงรายการสินค้า
        
        try:
            os.makedirs("output", exist_ok=True)
            output_dir = os.path.abspath("output")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"ใบเสร็จ_{order_no}.pdf")
            logging.info(f"📄 สร้างไฟล์ PDF ใบเสร็จที่: {output_path}")

            generate_invoice_pdf(order, items, output_path)

            logging.info("✅ สร้างใบเสร็จ PDF เสร็จสมบูรณ์")

            self.pdf_viewer = PDFViewer(output_path)
            self.pdf_viewer.show()

        except Exception as e:
            logging.error(f"❌ เกิดข้อผิดพลาดขณะสร้างใบเสร็จ: {e}", exc_info=True)
            QMessageBox.critical(self, "ผิดพลาด", f"ไม่สามารถสร้างใบเสร็จได้: {e}")

    def on_order_table_clicked(self, index):
        if not index.isValid():
            return

        col = index.column()
        row = index.row()

        # สมมติคอลัมน์สถานะคำสั่งซื้อคือ 5
        if col == 5:
            model = self.orderTableView.model()
            order = model.orders[row]
            current_status = order.get("order_payment_status", "รอดำเนินการ")

            dialog = UpdateOrderStatusDialog(current_status, self)
            if dialog.exec():
                new_status = dialog.get_selected_status()
                order_no = order["order_no"]

                # อัพเดตสถานะในฐานข้อมูลผ่าน controller
                self.orderController.update_payment_status(order_no, new_status)

                # รีเฟรชข้อมูลใหม่
                self.load_order_data()

    def on_tab_changed(self, index):
        tab_name = self.tabWidget.tabText(index)
        logging.info(f"🔄 เปลี่ยนแท็บไปที่: {tab_name}")

        if tab_name == "ใบส่งของ":
            self.load_order_data()

        elif tab_name == "ใบกำกับภาษี":
            self.invoice_model.refresh_data()  # สร้างเมธอดนี้ใน `InvoiceTableModel` ถ้ายังไม่มี
            self.tableView_invoices.resizeColumnsToContents()
            self.tableView_invoices.setColumnWidth(6, 140)     # ตั้งขนาดคอลัมน์ปุ่มใหม่

