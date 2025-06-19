from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QApplication, QStyle
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QObject
from PyQt6.QtGui import QMouseEvent, QPainter, QColor, QBrush, QFont, QPen

class ButtonClickSignal(QObject):
    clicked = pyqtSignal(int)

class ModernButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, label="📄 ปุ่ม", color="#2196F3"):
        super().__init__(parent)
        self.label = label
        self.color = color  # สีพื้นหลังปุ่ม
        self.button_signal = ButtonClickSignal()

    def paint(self, painter, option, index):
        painter.save()

        # ขนาดปุ่มคงที่
        button_width = 120
        button_height = 32
        radius = 10

        # คำนวณให้ปุ่มอยู่ตรงกลาง cell
        rect = QRect(
            option.rect.x() + (option.rect.width() - button_width) // 2,
            option.rect.y() + (option.rect.height() - button_height) // 2,
            button_width,
            button_height
        )

        # วาดปุ่ม
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(self.color)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # ข้อความบนปุ่ม
        painter.setPen(QPen(Qt.GlobalColor.white))
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.label)

        painter.restore()
        # painter.save()

        # # ปรับค่ามุมโค้ง และขนาด
        # rect = option.rect.adjusted(5, 5, -5, -5)
        # radius = 10

        # # ใช้สีจากพารามิเตอร์
        # painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # painter.setBrush(QBrush(QColor(self.color)))
        # painter.setPen(Qt.PenStyle.NoPen)
        # painter.drawRoundedRect(rect, radius, radius)

        # # ข้อความบนปุ่ม
        # painter.setPen(QPen(Qt.GlobalColor.white))
        # font = QFont("Arial", 12, QFont.Weight.Bold)
        # painter.setFont(font)
        # painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.label)

        # painter.restore()

    def editorEvent(self, event, model, option, index):
        if isinstance(event, QMouseEvent) and event.type() == event.Type.MouseButtonRelease:
            self.button_signal.clicked.emit(index.row())
        return True
