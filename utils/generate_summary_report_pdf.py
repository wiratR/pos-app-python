import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from utils.path_utils import resource_path

# ลงทะเบียนฟอนต์ TH Sarabun (ถ้ายังไม่ลงทะเบียน)
pdfmetrics.registerFont(TTFont('THSarabun', resource_path('resources/assets/fonts/THSarabunNew.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-Bold', resource_path('resources/assets/fonts/THSarabunNew Bold.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-Italic', resource_path('resources/assets/fonts/THSarabunNew Italic.ttf')))
pdfmetrics.registerFont(TTFont('THSarabun-BoldItalic', resource_path('resources/assets/fonts/THSarabunNew BoldItalic.ttf')))

def generate_summary_report_pdf(start_date: str, end_date: str, orders: list, output_path: str):
    """
    สร้าง PDF รายงานสรุปรายได้ ตามช่วงวันที่จ่ายเงิน

    :param start_date: วันที่เริ่มต้นในรูปแบบ 'YYYY-MM-DD'
    :param end_date: วันที่สิ้นสุดในรูปแบบ 'YYYY-MM-DD'
    :param orders: รายการคำสั่งซื้อที่จ่ายเงินแล้ว [{'order_no':..., 'total_amount':..., 'payment_complete_date':...}, ...]
    :param output_path: ที่อยู่ไฟล์ PDF ที่จะบันทึก
    """

    logging.info(f"📄 เริ่มสร้างรายงานสรุปรายได้: {output_path}")

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # หัวกระดาษ
    c.setFont("THSarabun-Bold", 18)
    c.drawString(2 * cm, height - 2 * cm, "รายงานสรุปรายได้")

    # ช่วงวันที่รายงาน
    c.setFont("THSarabun", 14)
    c.drawString(2 * cm, height - 3 * cm, f"ช่วงวันที่: {start_date} ถึง {end_date}")
    c.drawString(2 * cm, height - 3.8 * cm, f"วันที่ออกเอกสาร: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # หัวตาราง
    c.setFont("THSarabun-Bold", 14)
    start_y = height - 5 * cm
    c.drawString(2 * cm, start_y, "ลำดับ")
    c.drawString(4 * cm, start_y, "เลขที่คำสั่งซื้อ")
    c.drawString(14 * cm, start_y, "วันที่จ่ายเงิน")
    c.drawRightString(20 * cm, start_y, "จำนวนเงิน (บาท)")

    # รายการคำสั่งซื้อ
    c.setFont("THSarabun", 14)
    y = start_y - 1 * cm
    total_income = 0
    for i, order in enumerate(orders, start=1):
        order_no = order.get('order_no', '')
        pay_date = order.get('payment_complete_date', '')
        amount = float(order.get('total_amount', 0))

        c.drawString(2 * cm, y, str(i))
        c.drawString(4 * cm, y, order_no)
        c.drawString(14 * cm, y, pay_date)
        c.drawRightString(20 * cm, y, f"{amount:,.2f}")

        total_income += amount
        y -= 1 * cm

        # ขึ้นหน้าใหม่ถ้าเกินขอบล่าง
        if y < 2 * cm:
            c.showPage()
            c.setFont("THSarabun", 14)
            y = height - 2 * cm

    # รวมรายได้ทั้งหมด
    c.setFont("THSarabun-Bold", 16)
    c.drawRightString(20 * cm, y - 1 * cm, f"รวมรายได้ทั้งหมด: {total_income:,.2f} บาท")

    c.showPage()
    c.save()

    logging.info(f"✅ สร้างรายงานสรุปรายได้เสร็จสิ้นที่: {output_path}")
