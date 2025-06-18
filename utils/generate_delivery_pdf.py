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

def generate_delivery_pdf(order: dict, items: list, output_path: str):
    logging.info(f"📄 เริ่มสร้างใบส่งของ: {output_path}")

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    c.setTitle(f"Delivery Note - {order.get('order_no', 'unknown')}")
    c.setAuthor("บริษัทของคุณ")

    # === โลโก้ ===
    logo_path = resource_path("resources/assets/logo.png")
    if os.path.exists(logo_path):
        try:
            c.drawImage(logo_path, width - 6 * cm, height - 3.5 * cm,
                        width=5 * cm, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            logging.warning(f"⚠️ ไม่สามารถโหลดโลโก้: {e}")

    # === หัวเรื่อง ===
    c.setFont("THSarabun-Bold", 20)
    c.drawString(2 * cm, height - 2.5 * cm, "ใบส่งของ / Delivery Note")

    # === ข้อมูลคำสั่งซื้อ ===
    c.setFont("THSarabun", 16)
    c.drawString(2 * cm, height - 4 * cm, f"เลขที่ใบสั่งซื้อ: {order.get('order_no', '-')}")
    c.drawString(2 * cm, height - 4.8 * cm, f"วันที่: {datetime.today().strftime('%d/%m/%Y')}")

    # === ข้อมูลลูกค้า ===
    customer = order.get("customer", {})
    y = height - 6.2 * cm
    c.drawString(2 * cm, y, f"ชื่อลูกค้า: {customer.get('name', '-')}")
    c.drawString(2 * cm, y - 0.8 * cm, f"ที่อยู่: {customer.get('address', '-')}")
    c.drawString(2 * cm, y - 1.6 * cm, f"เบอร์โทร: {customer.get('phone', '-')}")

    # === ตารางสินค้า ===
    y = y - 3 * cm
    table_y = y
    c.setFont("THSarabun-Bold", 16)
    c.drawString(2 * cm, table_y, "รายการสินค้า")

    table_y -= 1.2 * cm
    c.setFont("THSarabun-Bold", 14)
    c.drawString(2 * cm, table_y, "สินค้า")
    c.drawString(10 * cm, table_y, "จำนวน")

    # เส้นบน
    c.line(2 * cm, table_y - 0.2 * cm, width - 2 * cm, table_y - 0.2 * cm)

    c.setFont("THSarabun", 14)
    table_y -= 1 * cm
    for item in items:
        c.drawString(2 * cm, table_y, item["product"])
        c.drawString(10 * cm, table_y, str(item["qty"]))
        table_y -= 0.8 * cm

    # เส้นล่าง
    c.line(2 * cm, table_y + 0.6 * cm, width - 2 * cm, table_y + 0.6 * cm)

    # === ลายเซ็นรับสินค้า ===
    table_y -= 2 * cm
    c.setFont("THSarabun", 14)
    c.drawString(2 * cm, table_y, "..............................................................")
    c.drawString(2 * cm, table_y - 0.8 * cm, "ผู้รับของ / Receiver")

    c.drawString(11 * cm, table_y, "..........................................................")
    c.drawString(11 * cm, table_y - 0.8 * cm, "วันที่เซ็นรับ / Received Date")

    # === บันทึกไฟล์ ===
    c.showPage()
    c.save()
    logging.info(f"✅ สร้างใบส่งของสำเร็จ: {output_path}")
