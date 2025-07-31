import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_pdf(customer, items, filename, notes=None):
    # Ensure the output directory exists
    output_dir = "generated_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Try to insert logo
    try:
        c.drawImage("static/logo.png", 30, height - 90, width=60, preserveAspectRatio=True)
    except Exception as e:
        print(f"Logo not found or could not be loaded: {e}")

    # Company Details aligned to the right
    c.setFont("Helvetica-Bold", 12)
    c.drawString(150, height - 50, "RATHI SONS ALGLAZE PVT. LTD.")
    c.setFont("Helvetica", 9)
    c.drawString(150, height - 65, "UPVC WINDOWS & DOORS FABRICATORS")
    c.drawString(150, height - 80, "Plot No.15, Sector B, Mandideep, Raisen, MP-462046")

    # Customer Information
    c.setFont("Helvetica-Bold", 10)
    y = height - 110
    c.drawString(30, y, f"To: {customer.name}")
    y -= 15
    c.setFont("Helvetica", 9)
    c.drawString(30, y, f"Place: {customer.place}")
    y -= 15
    c.drawString(30, y, f"Contact: {customer.contact}")
    y -= 15

    # Optional notes
    if notes:
        c.setFont("Helvetica-Bold", 9)
        y -= 10
        c.drawString(30, y, "Notes:")
        y -= 15
        c.setFont("Helvetica", 8)
        for line in notes.split('\n'):
            c.drawString(40, y, line)
            y -= 12

    # Table Header
    headers = ["Product", "Size", "Qty", "Area", "Price", "GST", "Total", "Glass", "Handle", "Color", "Series"]
    x_pos = [30, 90, 130, 160, 200, 240, 280, 330, 370, 410, 450, 500]
    y -= 25
    c.setFont("Helvetica-Bold", 8)
    for i, header in enumerate(headers):
        c.drawString(x_pos[i], y, header)

    # Table Data
    total_price = 0
    y -= 15
    c.setFont("Helvetica", 8)
    for item in items:
        if y < 100:
            c.showPage()
            y = height - 100
            for i, header in enumerate(headers):
                c.drawString(x_pos[i], y, header)
            y -= 15

        row = [
            item.product,
            f"{item.width}x{item.height}",
            item.quantity,
            f"{item.area:.2f}",
            f"{item.price:.2f}",
            f"{item.gst:.2f}",
            f"{item.total:.2f}",
            item.glass_type,
            item.handle,
            item.color,
            item.series
        ]
        for i, val in enumerate(row):
            c.drawString(x_pos[i], y, str(val))
        total_price += item.total
        y -= 15

    # Totals
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, f"Grand Total: ₹{total_price:.2f}")

    # Signature
    y -= 40
    c.setFont("Helvetica", 9)
    c.drawString(30, y, "Customer Signature")
    c.drawString(400, y, "Authorized Signatory")

    c.save()
