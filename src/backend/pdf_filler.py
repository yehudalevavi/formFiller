"""
PDF Form Filler using coordinate-based overlay with RTL support
"""
from io import BytesIO
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter
import arabic_reshaper
from bidi.algorithm import get_display
import os
from .field_mapping import FORM_FIELDS, HEBREW_FONT_SIZE, CHECKBOX_SIZE

# Signature field configurations - dual placement on page 4
SIGNATURE_CONFIGS = [
    {
        "page": 3,      # Page 4 (0-indexed)
        "x": 55,        # X position (left side)
        "y": 420,       # Y position - social worker signature area
        "width": 150,   # Max width
        "height": 40,   # Max height
    },
    {
        "page": 3,      # Page 4 (0-indexed)
        "x": 55,        # X position (left side)
        "y": 335,       # Y position - bottom signature area (near visit date)
        "width": 150,   # Max width
        "height": 40,   # Max height
    },
]

# Register Hebrew font
# Try embedded font first (for deployment), then fall back to system font (for local dev)
HEBREW_FONT_NAME = "NotoSansHebrew"
FONT_REGISTERED = False

# Get the project root directory (where fonts/ is located)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EMBEDDED_FONT_PATH = os.path.join(PROJECT_ROOT, "fonts", "NotoSansHebrew-Regular.ttf")
SYSTEM_FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"

try:
    if os.path.exists(EMBEDDED_FONT_PATH):
        pdfmetrics.registerFont(TTFont(HEBREW_FONT_NAME, EMBEDDED_FONT_PATH))
        FONT_REGISTERED = True
        print(f"Using embedded Hebrew font: {EMBEDDED_FONT_PATH}")
    elif os.path.exists(SYSTEM_FONT_PATH):
        pdfmetrics.registerFont(TTFont(HEBREW_FONT_NAME, SYSTEM_FONT_PATH))
        FONT_REGISTERED = True
        print(f"Using system Hebrew font: {SYSTEM_FONT_PATH}")
    else:
        HEBREW_FONT_NAME = "Helvetica"
        print(f"Warning: No Hebrew font found, using Helvetica")
except Exception as e:
    print(f"Error registering Hebrew font: {e}")
    HEBREW_FONT_NAME = "Helvetica"


class PDFFiller:
    def __init__(self, template_path):
        """Initialize PDF filler with template"""
        self.template_path = template_path
        self.reader = PdfReader(template_path)

    def prepare_hebrew_text(self, text):
        """Prepare Hebrew text for proper RTL display"""
        if not text:
            return ""
        # Reshape Arabic/Hebrew characters
        reshaped_text = arabic_reshaper.reshape(str(text))
        # Apply bidirectional algorithm
        bidi_text = get_display(reshaped_text)
        return bidi_text

    def _contains_hebrew(self, text):
        """Check if text contains Hebrew characters"""
        for char in text:
            if '\u0590' <= char <= '\u05FF':  # Hebrew Unicode range
                return True
        return False

    def _flatten_form_data(self, form_data, parent_key=''):
        """Flatten nested dictionaries in form data"""
        items = {}
        for key, value in form_data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                # Recursively flatten nested dicts
                items.update(self._flatten_form_data(value, new_key))
            else:
                items[new_key] = value
        return items

    def create_overlay(self, form_data):
        """Create overlay PDF with form data"""
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        # Extract signature data before flattening (use get to not modify original)
        signature_data = form_data.get('signature_image', None)

        # Flatten nested dictionaries first
        flat_data = self._flatten_form_data(form_data)

        # Group fields by page
        pages_data = {}
        for field_name, field_value in flat_data.items():
            if field_name not in FORM_FIELDS:
                continue

            field_config = FORM_FIELDS[field_name]
            page_num = field_config["page"]

            if page_num not in pages_data:
                pages_data[page_num] = []

            pages_data[page_num].append((field_name, field_value, field_config))

        # Determine the max page we need to draw on
        max_page = max(pages_data.keys()) if pages_data else 0
        if signature_data:
            max_page = max(max_page, max(cfg["page"] for cfg in SIGNATURE_CONFIGS))

        # Draw on each page
        for page_num in range(max_page + 1):
            if page_num > 0:
                can.showPage()

            # Draw form fields for this page
            if page_num in pages_data:
                for field_name, field_value, field_config in pages_data[page_num]:
                    self._draw_field(can, field_name, field_value, field_config)

            # Draw signatures at all designated locations on this page
            if signature_data:
                for sig_config in SIGNATURE_CONFIGS:
                    if page_num == sig_config["page"]:
                        self._draw_signature(can, signature_data, sig_config)

        can.save()
        packet.seek(0)
        return packet

    def _draw_field(self, can, field_name, field_value, field_config):
        """Draw a single field on the canvas with proper alignment"""
        x = field_config["x"]
        y = field_config["y"]
        align = field_config.get("align", "left")

        # Handle checkboxes
        if field_config.get("checkbox", False):
            if field_value in [True, "true", "yes", "כן", "1", 1]:
                can.setFont("Helvetica", CHECKBOX_SIZE)
                can.drawString(x, y, "X")
            return

        # Handle text fields
        if not field_value:
            return

        value_str = str(field_value)

        # Choose font based on content - Hebrew font doesn't support ASCII well
        if self._contains_hebrew(value_str):
            # Process Hebrew text with bidi algorithm
            text = self.prepare_hebrew_text(value_str)
            font_name = HEBREW_FONT_NAME
        else:
            # ASCII text - use Helvetica which renders numbers correctly
            text = value_str
            font_name = "Helvetica"

        can.setFont(font_name, HEBREW_FONT_SIZE)

        # Handle multiline text
        if field_config.get("multiline", False):
            max_width = field_config.get("width", 450)
            lines = self._wrap_text(text, max_width, can, font_name)

            # Draw each line
            line_height = field_config.get("line_height", HEBREW_FONT_SIZE + 3)
            current_y = y
            for line in lines[:10]:  # Limit to 10 lines
                if align == "right":
                    can.drawRightString(x, current_y, line)
                else:
                    can.drawString(x, current_y, line)
                current_y -= line_height
        else:
            # Single line text
            max_length = field_config.get("max_length", 100)
            if len(text) > max_length:
                text = text[:max_length]

            # Draw with proper alignment
            if align == "right":
                can.drawRightString(x, y, text)
            else:
                can.drawString(x, y, text)

    def _wrap_text(self, text, max_width, can, font_name):
        """Simple text wrapping with proper font width calculation"""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            # Use actual font for width calculation
            if can.stringWidth(test_line, font_name, HEBREW_FONT_SIZE) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def _draw_signature(self, can, signature_data, config):
        """Draw signature image on the canvas at specified location"""
        if not signature_data:
            return

        try:
            # Remove data URL prefix if present
            if signature_data.startswith('data:image'):
                # Extract base64 data after the comma
                signature_data = signature_data.split(',', 1)[1]

            # Decode base64 to bytes
            image_bytes = base64.b64decode(signature_data)
            image_io = BytesIO(image_bytes)

            # Create ImageReader from bytes
            img = ImageReader(image_io)

            # Get original image dimensions
            img_width, img_height = img.getSize()

            # Calculate scale to fit within max dimensions while preserving aspect ratio
            max_width = config["width"]
            max_height = config["height"]

            scale_x = max_width / img_width if img_width > 0 else 1
            scale_y = max_height / img_height if img_height > 0 else 1
            scale = min(scale_x, scale_y, 1)  # Don't scale up, only down

            final_width = img_width * scale
            final_height = img_height * scale

            # Draw the signature image
            x = config["x"]
            y = config["y"]

            can.drawImage(img, x, y, width=final_width, height=final_height, mask='auto')

        except Exception as e:
            print(f"Error drawing signature: {e}")

    def fill_form(self, form_data, output_path=None):
        """Fill the form with provided data"""
        # Create overlay
        overlay_pdf = self.create_overlay(form_data)
        overlay_reader = PdfReader(overlay_pdf)

        # Create output PDF
        writer = PdfWriter()

        # Merge overlay with template
        for page_num in range(len(self.reader.pages)):
            template_page = self.reader.pages[page_num]

            # If we have an overlay for this page, merge it
            if page_num < len(overlay_reader.pages):
                overlay_page = overlay_reader.pages[page_num]
                template_page.merge_page(overlay_page)

            writer.add_page(template_page)

        # Write to output
        if output_path:
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            return output_path
        else:
            # Return as bytes
            output = BytesIO()
            writer.write(output)
            output.seek(0)
            return output.read()

    def get_field_list(self):
        """Return list of all available fields"""
        return list(FORM_FIELDS.keys())


def fill_pdf_form(template_path, form_data, output_path=None):
    """Convenience function to fill PDF form from a template file path"""
    filler = PDFFiller(template_path)
    return filler.fill_form(form_data, output_path)


def fill_pdf_from_bytes(pdf_bytes, form_data, output_path=None):
    """Fill a PDF form from bytes (for uploaded files)"""
    filler = PDFFillerFromBytes(pdf_bytes)
    return filler.fill_form(form_data, output_path)


class PDFFillerFromBytes(PDFFiller):
    """PDF Filler that accepts PDF bytes instead of a file path"""

    def __init__(self, pdf_bytes):
        """Initialize PDF filler with PDF bytes"""
        self.pdf_bytes = pdf_bytes
        self.reader = PdfReader(BytesIO(pdf_bytes))
