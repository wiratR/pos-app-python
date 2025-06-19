import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from utils.path_utils import resource_path

# โหลดฟอนต์ภาษาไทย (ควรโหลดครั้งเดียวเท่านั้น)
pdfmetrics.registerFont(TTFont('THSarabun', resource_path('resources/assets/fonts/THSarabunNew.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-Bold', resource_path('resources/assets/fonts/THSarabunNew Bold.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-Italic', resource_path('resources/assets/fonts/THSarabunNew Italic.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-BoldItalic', resource_path('resources/assets/fonts/THSarabunNew BoldItalic.ttf')))

def generate_invoice_pdf(order: dict, items: list, output_path: str):
    logging.info(f"🧾 เริ่มสร้างใบกำกับภาษี: {output_path}")

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # หัวใบเสร็จ
    c.setFont("THSarabun-Bold", 18)
    c.drawString(2 * cm, height - 2 * cm, "ใบเสร็จรับเงิน / ใบกำกับภาษี")

    # ข้อมูลบริษัท
    c.setFont("THSarabun", 14)
    c.drawString(2 * cm, height - 3 * cm, "บริษัท ตัวอย่าง จำกัด")
    c.drawString(2 * cm, height - 3.8 * cm, "ที่อยู่: 123 ถนนสุขุมวิท เขตคลองเตย กรุงเทพฯ 10110")
    c.drawString(2 * cm, height - 4.6 * cm, "โทร: 02-123-4567  เลขประจำตัวผู้เสียภาษี: 0105551234567")

    # ข้อมูลลูกค้า
    c.setFont("THSarabun-Bold", 14)
    c.drawString(12 * cm, height - 3 * cm, f"ชื่อลูกค้า: {order.get('company_name', '')}")
    c.drawString(12 * cm, height - 3.8 * cm, f"ที่อยู่: {order.get('company_address', '')}")
    c.drawString(12 * cm, height - 4.6 * cm, f"เลขที่ภาษี: {order.get('tax_id', '')}")
    c.drawString(12 * cm, height - 5.4 * cm, f"วันที่: {order.get('order_date', datetime.now().strftime('%d/%m/%Y'))}")
    c.drawString(12 * cm, height - 6.2 * cm, f"เลขที่ใบเสร็จ: {order.get('order_no', '')}")

    # หัวตารางสินค้า
    start_y = height - 8 * cm
    c.setFont("THSarabun-Bold", 14)
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
        if y < 3 * cm:
            c.showPage()
            c.setFont("THSarabun", 14)
            y = height - 3 * cm

    # สรุปราคา
    subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
    vat = subtotal * 0.07
    total = subtotal + vat

    c.setFont("THSarabun-Bold", 16)
    c.drawRightString(20 * cm, y - 1 * cm, f"รวมเงิน: {subtotal:,.2f} บาท")
    c.drawRightString(20 * cm, y - 2 * cm, f"ภาษีมูลค่าเพิ่ม (7%): {vat:,.2f} บาท")
    c.drawRightString(20 * cm, y - 3 * cm, f"ยอดรวมสุทธิ: {total:,.2f} บาท")

    # ลายเซ็น
    c.setFont("THSarabun", 14)
    c.drawString(2 * cm, y - 5 * cm, "ลงชื่อ ....................................................... ผู้รับเงิน")
    c.drawString(12 * cm, y - 5 * cm, "ลงชื่อ ....................................................... ผู้อนุมัติ")

    c.showPage()
    c.save()
    logging.info(f"✅ สร้างใบเสร็จรับเงินสำเร็จที่: {output_path}")
