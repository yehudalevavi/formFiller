#!/usr/bin/env python3
"""
Coordinate debugging tool - creates a PDF with grid and field labels
to help identify correct positions for each form field
"""
import sys
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
import os

# Import field mapping
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from backend.field_mapping import FORM_FIELDS

# Register Hebrew font
HEBREW_FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
HEBREW_FONT_NAME = "ArialUnicode"

if os.path.exists(HEBREW_FONT_PATH):
    pdfmetrics.registerFont(TTFont(HEBREW_FONT_NAME, HEBREW_FONT_PATH))
else:
    HEBREW_FONT_NAME = "Helvetica"

def create_debug_overlay():
    """Create overlay with grid and field labels"""
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    width, height = letter

    # Draw grid for all 4 pages
    for page in range(4):
        if page > 0:
            can.showPage()

        # Draw grid lines every 50 points
        can.setStrokeColorRGB(0.8, 0.8, 0.8)
        can.setLineWidth(0.5)

        # Vertical lines
        for x in range(0, int(width), 50):
            can.line(x, 0, x, height)
            if x % 100 == 0:
                can.setFont("Helvetica", 6)
                can.drawString(x + 2, 5, str(x))

        # Horizontal lines
        for y in range(0, int(height), 50):
            can.line(0, y, width, y)
            if y % 100 == 0:
                can.setFont("Helvetica", 6)
                can.drawString(5, y + 2, str(y))

        # Draw field markers for this page
        can.setStrokeColorRGB(1, 0, 0)  # Red
        can.setFillColorRGB(0, 0, 1)    # Blue text

        for field_name, field_config in FORM_FIELDS.items():
            if field_config.get("page") == page:
                x = field_config["x"]
                y = field_config["y"]

                # Draw crosshair at field position
                can.setLineWidth(1)
                can.line(x - 10, y, x + 10, y)
                can.line(x, y - 10, x, y + 10)

                # Draw field name
                can.setFont("Helvetica", 6)
                label = f"{field_name[:20]}"
                can.drawString(x + 12, y - 3, label)

                # Draw coordinate
                can.setFont("Helvetica", 5)
                can.drawString(x + 12, y - 10, f"({x},{y})")

    can.save()
    packet.seek(0)
    return packet

def create_debug_pdf(template_path, output_path):
    """Create debug PDF with grid and markers"""
    print(f"Creating debug PDF...")
    print(f"Template: {template_path}")
    print(f"Output: {output_path}")

    # Read template
    template_pdf = PdfReader(template_path)
    overlay_pdf = PdfReader(create_debug_overlay())

    # Merge overlay with template
    writer = PdfWriter()

    for page_num in range(min(len(template_pdf.pages), 4)):
        template_page = template_pdf.pages[page_num]

        if page_num < len(overlay_pdf.pages):
            overlay_page = overlay_pdf.pages[page_num]
            template_page.merge_page(overlay_page)

        writer.add_page(template_page)

    # Write output
    with open(output_path, 'wb') as f:
        writer.write(f)

    print(f"\nDebug PDF created at: {output_path}")
    print("\nThis PDF shows:")
    print("- Grid lines every 50 points (labeled every 100)")
    print("- Red crosshairs at each field position")
    print("- Blue labels showing field names and coordinates")
    print("\nUse this to identify correct coordinates for each field")

if __name__ == "__main__":
    template_path = "templates/template.pdf"
    output_path = "debug_coordinates.pdf"

    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}")
        sys.exit(1)

    create_debug_pdf(template_path, output_path)

    # Open the debug PDF
    os.system(f"open {output_path}")
