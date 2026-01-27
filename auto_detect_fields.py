#!/usr/bin/env python3
"""
Automatic field detection - analyzes PDF to find field positions and pre-filled values
"""
import pdfplumber
import json
import re
from collections import defaultdict

def analyze_pdf_fields(pdf_path):
    """Extract text with positions and identify field structure"""

    results = {
        "pages": [],
        "prefilled_fields": {},
        "empty_fields": {},
        "field_positions": {}
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"\n{'='*60}")
            print(f"PAGE {page_num + 1}")
            print(f"{'='*60}")

            page_data = {
                "page_number": page_num,
                "width": page.width,
                "height": page.height,
                "elements": []
            }

            # Extract words with positions
            words = page.extract_words(
                keep_blank_chars=True,
                x_tolerance=3,
                y_tolerance=3
            )

            # Group words by approximate y-position (same row)
            rows = defaultdict(list)
            for word in words:
                # Round y to group words on same line
                y_key = round(word['top'] / 5) * 5
                rows[y_key].append(word)

            # Sort rows by y position (top to bottom)
            for y_key in sorted(rows.keys()):
                row_words = sorted(rows[y_key], key=lambda w: w['x0'], reverse=True)  # RTL

                row_text = ' '.join([w['text'] for w in row_words])
                if row_words:
                    # Get row boundaries
                    y_top = min(w['top'] for w in row_words)
                    y_bottom = max(w['bottom'] for w in row_words)
                    y_center = page.height - ((y_top + y_bottom) / 2)  # Convert to PDF coords (from bottom)

                    print(f"\nRow at y={y_center:.0f} (from bottom):")
                    print(f"  Text: {row_text[:100]}")

                    # Analyze each word position
                    for w in row_words:
                        x_right = page.width - w['x0']  # Convert for RTL
                        x_left = page.width - w['x1']
                        word_y = page.height - w['top']

                        element = {
                            "text": w['text'],
                            "x": round(x_left),
                            "y": round(word_y),
                            "width": round(w['x1'] - w['x0']),
                        }
                        page_data["elements"].append(element)

            # Extract tables to understand structure
            tables = page.extract_tables()
            if tables:
                print(f"\n  Found {len(tables)} table(s)")
                for t_idx, table in enumerate(tables):
                    print(f"\n  Table {t_idx + 1}:")
                    for row_idx, row in enumerate(table[:5]):  # First 5 rows
                        print(f"    Row {row_idx}: {row}")

            results["pages"].append(page_data)

    return results

def identify_form_fields(pdf_path):
    """
    Identify form field labels and their expected input positions
    Based on Hebrew RTL layout
    """

    # Known field labels in Hebrew and their corresponding field names
    field_labels = {
        "תאריך הביקור": "visit_date",
        "שם הלשכה": "office_name",
        "שם העובד הסוציאלי האחראי": "social_worker_name",
        "טלפון נייד": "mobile_phone",
        "טלפון קווי": "landline_phone",
        "שם משפחה": "last_name",
        "שם פרטי": "first_name",
        "מספר זהות": "id_number",
        "מספר תעודת זהות": "id_number",
        "רחוב": "street",
        "מספר בית": "house_number",
        "כניסה": "entrance",
        "דירה": "apartment",
        "ישוב": "city",
        "מיקוד": "zipcode",
        "דואר אלקטרוני": "email",
        "מספר דרכון": "passport",
        "ארץ מוצא": "country",
        "תאריך תחילת השמה": "start_date",
    }

    field_positions = {}
    prefilled_values = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            words = page.extract_words(keep_blank_chars=True)

            # Create a mapping of label positions
            for word in words:
                text = word['text'].strip()

                # Check if this is a known label
                for label, field_name in field_labels.items():
                    if label in text or text in label:
                        # The input field is typically to the LEFT of the label in RTL
                        x_pos = word['x0']  # Left edge of label
                        y_pos = page.height - word['top']  # Convert to bottom-origin

                        key = f"{field_name}_page{page_num}"
                        field_positions[key] = {
                            "label": text,
                            "label_x": round(page.width - word['x1']),
                            "input_x": round(page.width - word['x0'] - 100),  # Input to left of label
                            "y": round(y_pos),
                            "page": page_num
                        }

    return field_positions

def extract_detailed_layout(pdf_path):
    """Extract detailed layout information for accurate field positioning"""

    print("\n" + "="*80)
    print("DETAILED FIELD POSITION ANALYSIS")
    print("="*80)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"\n\n{'#'*60}")
            print(f"# PAGE {page_num + 1} - Size: {page.width:.1f} x {page.height:.1f}")
            print(f"{'#'*60}")

            # Get all characters with exact positions
            chars = page.chars

            # Group characters into text runs
            if chars:
                # Sort by position
                chars_sorted = sorted(chars, key=lambda c: (c['top'], -c['x0']))

                current_line = []
                current_top = None

                lines = []
                for char in chars_sorted:
                    if current_top is None or abs(char['top'] - current_top) < 5:
                        current_line.append(char)
                        current_top = char['top']
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = [char]
                        current_top = char['top']

                if current_line:
                    lines.append(current_line)

                # Print lines with positions
                for line in lines[:50]:  # First 50 lines
                    text = ''.join([c['text'] for c in sorted(line, key=lambda c: -c['x0'])])
                    if text.strip():
                        y_pdf = page.height - line[0]['top']
                        x_start = page.width - max(c['x1'] for c in line)
                        x_end = page.width - min(c['x0'] for c in line)
                        print(f"y={y_pdf:6.1f} | x={x_start:5.1f}-{x_end:5.1f} | {text[:60]}")

if __name__ == "__main__":
    pdf_path = "templates/template.pdf"

    print("Analyzing PDF structure...")
    extract_detailed_layout(pdf_path)
