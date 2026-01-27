"""
PDF Validator - Validates uploaded PDFs match expected template structure
"""
from io import BytesIO
from pypdf import PdfReader


# Expected template specifications
EXPECTED_PAGE_COUNT = 4
EXPECTED_PAGE_WIDTH = 612  # US Letter width in points
EXPECTED_PAGE_HEIGHT = 792  # US Letter height in points
SIZE_TOLERANCE = 5  # Allow small variations in page size


def validate_uploaded_pdf(pdf_bytes, template_path):
    """
    Validate that an uploaded PDF matches the expected template structure.

    Args:
        pdf_bytes: The uploaded PDF file as bytes
        template_path: Path to the reference template PDF

    Returns:
        dict with 'valid' boolean and 'errors' list if invalid,
        or 'warnings' list for non-critical issues
    """
    errors = []
    warnings = []

    try:
        # Load the uploaded PDF
        uploaded_pdf = PdfReader(BytesIO(pdf_bytes))
    except Exception as e:
        return {
            'valid': False,
            'errors': [f'Unable to read PDF file: {str(e)}']
        }

    # Load the template PDF for comparison
    try:
        template_pdf = PdfReader(template_path)
    except Exception as e:
        return {
            'valid': False,
            'errors': [f'Unable to read template PDF: {str(e)}']
        }

    # Validation 1: Check page count
    uploaded_page_count = len(uploaded_pdf.pages)
    template_page_count = len(template_pdf.pages)

    if uploaded_page_count != template_page_count:
        errors.append(
            f'Page count mismatch: uploaded PDF has {uploaded_page_count} pages, '
            f'expected {template_page_count} pages'
        )

    # Validation 2: Check page sizes for each page
    for page_num in range(min(uploaded_page_count, template_page_count)):
        uploaded_page = uploaded_pdf.pages[page_num]
        template_page = template_pdf.pages[page_num]

        # Get page dimensions
        uploaded_box = uploaded_page.mediabox
        template_box = template_page.mediabox

        uploaded_width = float(uploaded_box.width)
        uploaded_height = float(uploaded_box.height)
        template_width = float(template_box.width)
        template_height = float(template_box.height)

        # Check width
        if abs(uploaded_width - template_width) > SIZE_TOLERANCE:
            errors.append(
                f'Page {page_num + 1} width mismatch: '
                f'{uploaded_width:.1f} vs expected {template_width:.1f} points'
            )

        # Check height
        if abs(uploaded_height - template_height) > SIZE_TOLERANCE:
            errors.append(
                f'Page {page_num + 1} height mismatch: '
                f'{uploaded_height:.1f} vs expected {template_height:.1f} points'
            )

    # Validation 3: Check for encryption/password protection
    if uploaded_pdf.is_encrypted:
        errors.append('PDF is encrypted or password-protected')

    # Validation 4: Basic structure checks
    try:
        # Try to access page content to ensure PDF is readable
        for page_num in range(uploaded_page_count):
            _ = uploaded_pdf.pages[page_num].extract_text()
    except Exception as e:
        warnings.append(f'Warning: Could not extract text from PDF: {str(e)}')

    # Validation 5: Check for form fields (if template has them)
    # This is informational - the overlay approach doesn't require form fields
    if uploaded_pdf.get_fields():
        warnings.append('PDF contains form fields - they will be preserved but not used')

    result = {
        'valid': len(errors) == 0,
        'errors': errors if errors else None,
        'warnings': warnings if warnings else None,
        'info': {
            'page_count': uploaded_page_count,
            'encrypted': uploaded_pdf.is_encrypted,
            'has_form_fields': bool(uploaded_pdf.get_fields())
        }
    }

    # Remove None values
    result = {k: v for k, v in result.items() if v is not None}

    return result


def get_pdf_info(pdf_bytes):
    """
    Get information about a PDF file.

    Args:
        pdf_bytes: The PDF file as bytes

    Returns:
        dict with PDF information
    """
    try:
        pdf = PdfReader(BytesIO(pdf_bytes))

        pages_info = []
        for i, page in enumerate(pdf.pages):
            box = page.mediabox
            pages_info.append({
                'page': i + 1,
                'width': float(box.width),
                'height': float(box.height)
            })

        return {
            'page_count': len(pdf.pages),
            'encrypted': pdf.is_encrypted,
            'has_form_fields': bool(pdf.get_fields()),
            'pages': pages_info,
            'metadata': dict(pdf.metadata) if pdf.metadata else None
        }
    except Exception as e:
        return {'error': str(e)}
