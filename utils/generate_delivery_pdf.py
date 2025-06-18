# utils/generate_delivery_pdf.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime

def generate_delivery_pdf(order: dict, items: list, output_path: str):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # === โลโก้บริษัท (ถ้ามี) ===
    logo_path = "resources/assets/logo.png"
    try:
        c.drawImage(logo_path, width - 5*cm, height - 3*cm, width=4*cm, preserveAspectRatio=True)
    except:
        pass  # ถ้าไม่มีโลโก้ให้ข้ามไป

    # === หัวกระดาษ ===
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, "ใบส่งของ / Delivery Note")

    # === ข้อมูลคำสั่งซื้อ ===
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, height - 3.5 * cm, f"เลขที่ใบสั่งซื้อ: {order.get('order_no', '-')}")
    c.drawString(2 * cm, height - 4.2 * cm, f"วันที่: {datetime.today().strftime('%d/%m/%Y')}")

    # === ข้อมูลลูกค้า ===
    y = height - 5.5 * cm
    customer = order.get("customer", {})
    c.drawString(2 * cm, y, f"ชื่อลูกค้า: {customer.get('name', '-')}")
    c.drawString(2 * cm, y - 0.7 * cm, f"ที่อยู่: {customer.get('address', '-')}")
    c.drawString(2 * cm, y - 1.4 * cm, f"เบอร์โทร: {customer.get('phone', '-')}")

    # === ตารางรายการสินค้า ===
    y = y - 2.5 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "รายการสินค้า")
    c.setFont("Helvetica", 11)

    table_y = y - 1 * cm
    c.drawString(2 * cm, table_y, "สินค้า")
    c.drawString(9 * cm, table_y, "จำนวน")

    c.line(2 * cm, table_y - 0.2 * cm, width - 2 * cm, table_y - 0.2 * cm)

    table_y -= 0.8 * cm
    for item in items:
        c.drawString(2 * cm, table_y, item["product"])
        c.drawString(9 * cm, table_y, str(item["qty"]))
        table_y -= 0.6 * cm

    # === เซ็นรับสินค้า ===
    c.drawString(2 * cm, table_y - 1.2 * cm, "..................................................")
    c.drawString(2 * cm, table_y - 2.0 * cm, "ผู้รับของ / Receiver")

    c.drawString(11 * cm, table_y - 1.2 * cm, "..................................................")
    c.drawString(11 * cm, table_y - 2.0 * cm, "วันที่เซ็นรับ / Received Date")

    # === บันทึก PDF ===
    c.showPage()
    c.save()
