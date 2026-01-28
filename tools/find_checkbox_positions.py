#!/usr/bin/env python3
"""
Script to analyze PDF template and find checkbox positions
Uses pdfplumber to extract text positions and identify checkbox areas
"""
import pdfplumber

# Keywords that indicate checkbox areas
CHECKBOX_KEYWORDS = [
    # Page 1
    ("ישראל", "חו\"ל"),  # placement checkboxes
    # Page 2
    ("כן", "לא"),  # yes/no checkboxes
    # Page 3
    ("מעסיק", "עובד", "אחר"),  # contract checkboxes
    ("שיק", "הפקדה", "מזומן"),  # payment checkboxes
    # Page 4
    ("טיפול", "גישור", "מעקב", "הפניה", "דיווח"),  # treatment checkboxes
    ("נוכחים",),  # attendees
]

def analyze_pdf_for_checkboxes(pdf_path):
    """Extract all text with positions to find checkbox locations"""
    print(f"Analyzing: {pdf_path}\n")
    print("=" * 80)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"\n{'='*80}")
            print(f"PAGE {page_num + 1} (index {page_num})")
            print(f"Page size: {page.width} x {page.height}")
            print("=" * 80)

            # Get all characters with their positions
            chars = page.chars

            # Group characters into words/phrases with positions
            words = page.extract_words(
                x_tolerance=3,
                y_tolerance=3,
                keep_blank_chars=True
            )

            # Find checkbox-related words
            checkbox_words = []
            for word in words:
                text = word['text'].strip()
                # Look for common checkbox indicators
                if text in ['כן', 'לא', 'ישראל', "חו\"ל", 'מעסיק', 'עובד', 'אחר',
                           'שיק', 'הפקדה', 'מזומן', 'גישור', 'מעקב', 'הפניה', 'דיווח',
                           'בעיות', 'טיפול', 'ךווית', 'חוויד', 'גושיר', 'בקעמ']:
                    checkbox_words.append(word)
                # Also look for checkbox-like patterns (small boxes next to text)
                if len(text) <= 15 and any(kw in text for kw in ['טיפול', 'נוכח', 'תשלום', 'חוזה']):
                    checkbox_words.append(word)

            # Print relevant findings
            print(f"\nFound {len(checkbox_words)} checkbox-related words:")
            for word in sorted(checkbox_words, key=lambda w: (-w['top'], -w['x0'])):
                # Convert to PDF coordinates (from top-left to bottom-left origin)
                pdf_y = page.height - word['top']
                print(f"  '{word['text']}' at x={word['x0']:.1f}, y={pdf_y:.1f} (top={word['top']:.1f})")

            # Also look for small rectangles that might be checkbox boxes
            rects = page.rects
            small_rects = [r for r in rects if
                          8 <= r['width'] <= 15 and
                          8 <= r['height'] <= 15]

            if small_rects:
                print(f"\nPotential checkbox boxes ({len(small_rects)} small rectangles):")
                for rect in sorted(small_rects, key=lambda r: (-r['top'], -r['x0'])):
                    pdf_y = page.height - rect['top']
                    print(f"  Box at x={rect['x0']:.1f}, y={pdf_y:.1f} (size: {rect['width']:.1f}x{rect['height']:.1f})")

def find_all_text_near_checkboxes(pdf_path):
    """Find all text elements to understand checkbox context"""
    print("\n" + "=" * 80)
    print("DETAILED TEXT ANALYSIS FOR CHECKBOX AREAS")
    print("=" * 80)

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            print(f"\n--- Page {page_num + 1} ---")

            words = page.extract_words(x_tolerance=2, y_tolerance=2)

            # Group by approximate Y position (rows)
            rows = {}
            for word in words:
                # Round Y to group nearby text
                y_key = round(word['top'] / 10) * 10
                if y_key not in rows:
                    rows[y_key] = []
                rows[y_key].append(word)

            # Print rows that likely contain checkboxes
            for y_key in sorted(rows.keys()):
                row_words = rows[y_key]
                row_text = ' | '.join([w['text'] for w in sorted(row_words, key=lambda x: -x['x0'])])

                # Check if this row might have checkboxes
                has_checkbox_indicator = any(
                    kw in row_text for kw in
                    ['כן', 'לא', 'ישראל', 'חו"ל', 'מעסיק', 'עובד', 'אחר',
                     'שיק', 'הפקדה', 'מזומן', 'טיפול', 'גישור', 'מעקב',
                     'הפניה', 'דיווח', 'נוכח', 'משפחה']
                )

                if has_checkbox_indicator:
                    pdf_y = page.height - y_key
                    print(f"\nY≈{pdf_y:.0f} (top={y_key}): {row_text[:200]}")
                    # Print individual word positions
                    for w in sorted(row_words, key=lambda x: -x['x0']):
                        w_pdf_y = page.height - w['top']
                        print(f"    '{w['text']}' x0={w['x0']:.1f}, x1={w['x1']:.1f}, y={w_pdf_y:.1f}")

if __name__ == "__main__":
    template_path = "templates/template.pdf"

    print("CHECKBOX POSITION ANALYSIS")
    print("=" * 80)

    analyze_pdf_for_checkboxes(template_path)
    find_all_text_near_checkboxes(template_path)
