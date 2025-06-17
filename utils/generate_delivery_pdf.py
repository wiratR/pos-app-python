# utils/generate_delivery_pdf.py

from reportbro.report import Report
import os

def generate_delivery_pdf(order_data, items, output_path):
    template_path = os.path.join("templates", "delivery_note.json")
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        report_definition = f.read()

    report = Report(report_definition, parameters={
        "order_no": order_data["order_no"],
        "order_date": order_data["order_date"],
        "delivery_date": order_data["delivery_date"],
        "customer": order_data["company_name"],
        "total_amount": order_data["total_amount"],
        "items": items,
    })

    with open(output_path, "wb") as f:
        f.write(report.generate_pdf())
