import os
import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QGroupBox, QSpinBox,
    QLineEdit, QPushButton, QMessageBox, QCalendarWidget, QTableView,
    QInputDialog
)
from PyQt6.QtCore import QTimer, QModelIndex
from PyQt6.uic import loadUi

# 👇 Add import for product model
from models.product_model import ProductModel
from models.product_table_model import ProductTableModel
from views.add_product_dialog import AddProductDialog   # import the dialog
from views.edit_product_dialog import EditProductDialog  # import the dialog


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


class HomeView(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_file = resource_path(os.path.join("views", "home_view.ui"))
        loadUi(ui_file, self)
        logging.info("🔧 Loading HomeView UI from %s", ui_file)

        self.showFullScreen()  # 👈 This line enables full-screen view

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

    # def add_product(self):
    #     name, ok1 = QInputDialog.getText(self, "เพิ่มสินค้า", "ชื่อสินค้า:")
    #     if not ok1 or not name:
    #         return

    #     description, ok2 = QInputDialog.getText(self, "เพิ่มสินค้า", "รายละเอียดสินค้า:")
    #     if not ok2:
    #         return

    #     price_str, ok3 = QInputDialog.getText(self, "เพิ่มสินค้า", "ราคาสินค้า:")
    #     if not ok3:
    #         return

    #     try:
    #         price = float(price_str)
    #     except ValueError:
    #         QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณาระบุราคาเป็นตัวเลข")
    #         return

    #     # Add to DB and refresh table
    #     self.tableView.model().product_model.add_product(name, description, price)
    #     self.tableView.model()._products = self.tableView.model().product_model.get_all_products()
    #     self.tableView.model().layoutChanged.emit()

    #     QMessageBox.information(self, "เพิ่มสินค้า", "เพิ่มสินค้าเรียบร้อยแล้ว")
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
