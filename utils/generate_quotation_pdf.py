import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from utils.path_utils import resource_path  # ให้แน่ใจว่าใช้ resource_path แบบปลอดภัย

# 🔤 Register TH Sarabun Fonts
pdfmetrics.registerFont(TTFont('THSarabun', resource_path('resources/assets/fonts/THSarabunNew.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-Bold', resource_path('resources/assets/fonts/THSarabunNew Bold.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-Italic', resource_path('resources/assets/fonts/THSarabunNew Italic.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-BoldItalic', resource_path('resources/assets/fonts/THSarabunNew BoldItalic.ttf')))

def generate_quotation_pdf(order: dict, items: list, output_path: str):
    logging.info(f"📄 เริ่มสร้างใบเสนอราคา: {output_path}")

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # ตั้งฟอนต์เริ่มต้น
    c.setFont("THSarabun-Bold", 18)
    c.drawString(2 * cm, height - 2 * cm, "ใบเสนอราคา (Quotation)")

    # ข้อมูลบริษัท / ผู้ขาย (ตัวอย่าง)
    c.setFont("THSarabun", 14)
    c.drawString(2 * cm, height - 3 * cm, "บริษัท ตัวอย่าง จำกัด")
    c.drawString(2 * cm, height - 3.8 * cm, "ที่อยู่: 123 ถนนสุขุมวิท เขตคลองเตย กรุงเทพฯ")
    c.drawString(2 * cm, height - 4.6 * cm, "โทร: 02-123-4567")

    # ข้อมูลลูกค้า
    c.setFont("THSarabun-Bold", 14)
    c.drawString(12 * cm, height - 3 * cm, f"ลูกค้า: {order.get('customer_name', '')}")
    c.drawString(12 * cm, height - 3.8 * cm, f"ที่อยู่: {order.get('customer_address', '')}")
    c.drawString(12 * cm, height - 4.6 * cm, f"วันที่: {order.get('date', datetime.now().strftime('%d/%m/%Y'))}")
    c.drawString(12 * cm, height - 5.4 * cm, f"เลขที่ใบเสนอราคา: {order.get('quotation_id', '')}")

    # หัวตารางสินค้า
    c.setFont("THSarabun-Bold", 14)
    start_y = height - 7 * cm
    c.drawString(2 * cm, start_y, "ลำดับ")
    c.drawString(3 * cm, start_y, "รายการสินค้า")
    c.drawString(12 * cm, start_y, "จำนวน")
    c.drawString(15 * cm, start_y, "ราคาต่อหน่วย")
    c.drawString(18 * cm, start_y, "ราคารวม")

    # รายการสินค้า
    c.setFont("THSarabun", 14)
    y = start_y - 1 * cm
    for i, item in enumerate(items, start=1):
        quantity = item.get('quantity', 0)
        unit_price = item.get('unit_price', 0)
        total_price = quantity * unit_price

        c.drawString(2 * cm, y, str(i))
        c.drawString(3 * cm, y, item.get('name', ''))
        c.drawRightString(14 * cm, y, str(quantity))
        c.drawRightString(17 * cm, y, f"{unit_price:,.2f}")
        c.drawRightString(20 * cm, y, f"{total_price:,.2f}")

        y -= 1 * cm
        # ถ้ารายการเยอะเกินหน้ากระดาษ ให้ขึ้นหน้าใหม่
        if y < 2 * cm:
            c.showPage()
            c.setFont("THSarabun", 14)
            y = height - 2 * cm

    # รวมราคารวมทั้งหมด
    total = sum(item.get('quantity', 0) * item.get('unit_price', 0) for item in items)
    c.setFont("THSarabun-Bold", 16)
    c.drawRightString(20 * cm, y - 1 * cm, f"รวมทั้งสิ้น: {total:,.2f} บาท")

    # ข้อความท้ายใบเสนอราคา (ถ้ามี)
    note = order.get('note', '')
    if note:
        c.setFont("THSarabun-Italic", 12)
        c.drawString(2 * cm, y - 3 * cm, f"หมายเหตุ: {note}")

    c.showPage()
    c.save()

    logging.info(f"✅ สร้างใบเสนอราคาเสร็จสิ้นที่: {output_path}")