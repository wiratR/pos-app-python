from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QApplication, QStyle
from PyQt6.QtCore import Qt, QRect, pyqtSignal, QObject
from PyQt6.QtGui import QMouseEvent, QPainter, QColor, QBrush, QFont, QPen

class ButtonClickSignal(QObject):
    clicked = pyqtSignal(int)

class ModernButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_signal = ButtonClickSignal()

    def paint(self, painter, option, index):
        painter.save()

        # ปรับค่ามุมโค้ง และขนาด
        rect = option.rect.adjusted(5, 5, -5, -5)
        radius = 10

        # สีพื้นหลังฟ้า
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor("#2196F3")))  # สีฟ้า
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, radius, radius)

        # ข้อความบนปุ่ม
        painter.setPen(QPen(Qt.GlobalColor.white))
        font = QFont("Segoe UI", 10, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "📄 ใบส่งของ")

        painter.restore()

    def editorEvent(self, event, model, option, index):
        if isinstance(event, QMouseEvent) and event.type() == event.Type.MouseButtonRelease:
            self.button_signal.clicked.emit(index.row())
        return True
