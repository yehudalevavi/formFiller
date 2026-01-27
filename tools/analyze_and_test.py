#!/usr/bin/env python3
"""
Analyze PDF and create test with sample data to verify coordinates
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter
import arabic_reshaper
from bidi.algorithm import get_display

# Register Hebrew font
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(PROJECT_ROOT, "fonts", "NotoSansHebrew-Regular.ttf")
SYSTEM_FONT = "/Library/Fonts/Arial Unicode.ttf"

if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont("HebrewFont", FONT_PATH))
    HEBREW_FONT = "HebrewFont"
elif os.path.exists(SYSTEM_FONT):
    pdfmetrics.registerFont(TTFont("HebrewFont", SYSTEM_FONT))
    HEBREW_FONT = "HebrewFont"
else:
    HEBREW_FONT = "Helvetica"

def prepare_hebrew(text):
    """Prepare Hebrew text for RTL display"""
    if not text:
        return ""
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

def create_test_overlay_page1():
    """Create test overlay for page 1 with sample data at calculated positions"""
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    width, height = A4  # 595.3 x 841.9

    # ===== PAGE 1 TEST DATA =====
    can.setFont("Helvetica", 9)

    # Based on PDF analysis:
    # Labels at y_from_top=136, y_from_bottom ≈ 706 (841.9 - 136)
    # Input should be below labels

    # Visit date - labels are at y≈706, inputs should be at y≈690
    # Day label x0=56.1, Month label x0=71.5, Year label x0=101.7
    # For RTL: numbers go left-to-right, but field position should be under label

    test_data = {
        # Date fields - positioned under their labels
        # Day at x=56-64, below at y≈688
        ("15", 58, 688, False),  # day (2 digits)
        ("08", 75, 688, False),  # month
        ("2024", 100, 688, False),  # year

        # Employer details - labels at y≈616, inputs at y≈598
        # שם משפחה label x0=504-547, input should END at x≈547
        ("כהן", 547, 598, True),  # last name - right aligned
        ("דוד", 425, 598, True),  # first name - right aligned to x≈425
        ("123456789", 235, 598, False),  # ID - numbers at x≈195-235

        # Employer address - labels at y≈570, inputs at y≈552
        ("הרצל", 547, 552, True),  # street - right aligned
        ("42", 425, 552, False),  # house number
        ("א", 376, 552, True),  # entrance
        ("5", 337, 552, False),  # apartment
        ("תל אביב", 298, 552, True),  # city - right aligned
        ("6100000", 131, 552, False),  # zipcode

        # Contact - labels at y≈535, inputs at y≈517
        ("03-1234567", 547, 517, False),  # landline
        ("054-1234567", 425, 517, False),  # mobile
        ("test@email.com", 297, 517, False),  # email

        # Worker passport - label at y≈496, input at y≈482
        ("AB1234567", 300, 482, False),  # passport

        # Worker names - labels at y≈479, inputs at y≈461
        ("גרסיה", 547, 461, True),  # last name - right aligned
        ("מריה", 425, 461, True),  # first name
        ("פיליפינים", 287, 461, True),  # origin country
        ("050-9876543", 154, 461, False),  # mobile

        # Placement - labels at y≈449, inputs at y≈432
        ("01/01/2024", 521, 432, False),  # start date

        # Worker address - labels at y≈417, inputs at y≈400
        ("דיזנגוף", 489, 400, True),  # street
        ("100", 378, 400, False),  # house number
        ("ב", 331, 400, True),  # entrance
        ("3", 290, 400, False),  # apartment
        ("תל אביב", 255, 400, True),  # city
        ("שישי", 105, 400, True),  # day off

        # Previous visits - labels at y≈359, inputs at y≈345
        ("15/12/2023", 538, 345, False),  # pre date
        ("יעל לוי", 459, 345, True),  # pre social worker
        ("01/02/2024", 318, 345, False),  # post date
        ("רחל כהן", 234, 345, True),  # post social worker
    }

    for text, x, y, is_hebrew in test_data:
        if is_hebrew:
            can.setFont(HEBREW_FONT, 9)
            # For Hebrew RTL text, use drawRightString to align from right
            prepared = prepare_hebrew(text)
            can.drawRightString(x, y, prepared)
        else:
            can.setFont("Helvetica", 9)
            can.drawString(x, y, text)

    # Draw reference markers for key positions
    can.setStrokeColorRGB(0.5, 0.5, 0.5)
    can.setDash(1, 2)

    # Draw light reference at key y positions
    for y in [688, 598, 552, 517, 482, 461, 432, 400, 345]:
        can.line(50, y, 550, y)

    can.save()
    packet.seek(0)
    return packet

def create_full_test():
    """Create test PDF with all pages filled"""
    template = PdfReader("templates/template.pdf")
    overlay = PdfReader(create_test_overlay_page1())

    writer = PdfWriter()

    # Merge page 1
    page = template.pages[0]
    page.merge_page(overlay.pages[0])
    writer.add_page(page)

    # Add remaining pages unchanged
    for i in range(1, len(template.pages)):
        writer.add_page(template.pages[i])

    output_path = "test_coordinates_v2.pdf"
    with open(output_path, 'wb') as f:
        writer.write(f)

    print(f"Created test PDF: {output_path}")
    return output_path

if __name__ == "__main__":
    output = create_full_test()
    os.system(f"open {output}")
