import os
import shutil
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QScrollArea, QVBoxLayout, QWidget,
    QPushButton, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QTimer, QSize

class PDFViewer(QMainWindow):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle("แสดงผลรายงาน PDF")
        
        # ลดขนาดหน้าต่างลงเหลือ 75% ของขนาดหน้าจอ
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        width = int(screen_size.width() * 0.75)
        height = int(screen_size.height() * 0.75)
        self.resize(width, height)

        self.pdf_path = pdf_path  # เก็บ path ไว้ใช้ใน save as

        # วาง layout หลัก
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # ปุ่ม Save as
        button_layout = QHBoxLayout()
        save_button = QPushButton("บันทึก ... (Save As)")
        save_button.clicked.connect(self.save_as)
        button_layout.addStretch()
        button_layout.addWidget(save_button)
        main_layout.addLayout(button_layout)

        # scroll area สำหรับแสดง pdf
        scroll_area = QScrollArea()
        container = QWidget()
        layout = QVBoxLayout(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(container)

        main_layout.addWidget(scroll_area)

        self.setCentralWidget(main_widget)

        # โหลด PDF
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            mode = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, mode)

            label = QLabel()
            label.setPixmap(QPixmap.fromImage(image))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout.addWidget(label)

        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)

        # ปรับสถานะหน้าต่างปกติ
        self.setWindowState(Qt.WindowState.WindowNoState)
        self.showNormal()
        self.show()

        QTimer.singleShot(100, lambda: (
            self.setWindowState(Qt.WindowState.WindowNoState),
            self.showNormal()
        ))

    def save_as(self):
        options = QFileDialog.Option.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF as",
            "delivery_note.pdf",
            "PDF Files (*.pdf);;All Files (*)",
            options=options
        )
        if file_path:
            try:
                if not os.path.exists(self.pdf_path):
                    QMessageBox.critical(self, "Error", f"ไม่พบไฟล์ต้นฉบับ: {self.pdf_path}")
                    return
                
                if os.path.abspath(self.pdf_path) == os.path.abspath(file_path):
                    QMessageBox.warning(self, "Warning", "ไม่สามารถบันทึกทับไฟล์เดิมได้")
                    return

                shutil.copyfile(self.pdf_path, file_path)
                QMessageBox.information(self, "สำเร็จ", f"บันทึกไฟล์สำเร็จที่:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"ไม่สามารถบันทึกไฟล์ได้: {e}")











