# Architecture Documentation

This document provides in-depth technical details for developers and AI agents working on this codebase.

## System Overview

The PDF Form Filler is a stateless web application that generates filled PDF forms by overlaying text and images onto a template PDF. The system is designed for simplicity, with no database, authentication, or persistent state.

## Core Components

### 1. Flask Application (`app.py`)

**Role**: HTTP server and API gateway

**Key Responsibilities**:
- Serve the HTML form interface
- Route API requests to appropriate handlers
- Handle file uploads (multipart/form-data)
- Return generated PDFs as downloadable files

**Configuration**:
```python
app.config['TEMPLATE_PDF'] = 'templates/template.pdf'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

**Request Flow**:
```
Client Request → Flask Route → Handler Function → Response
                    ↓
            pdf_filler.py (if PDF generation)
                    ↓
            field_mapping.py (field coordinates)
```

### 2. PDF Filler Module (`src/backend/pdf_filler.py`)

**Role**: Core PDF generation logic

**Classes**:

#### `PDFFiller`
Main class for PDF generation from template files.

```python
class PDFFiller:
    def __init__(self, template_path: str)
    def prepare_hebrew_text(self, text: str) -> str  # BiDi processing
    def create_overlay(self, form_data: dict) -> BytesIO  # Generate overlay PDF
    def fill_form(self, form_data: dict, output_path: str = None) -> bytes
```

#### `PDFFillerFromBytes`
Subclass for processing uploaded PDFs (bytes instead of file path).

**Key Implementation Details**:

1. **Overlay Approach**: Instead of editing the PDF directly, we create a transparent PDF with only the form data, then merge it with the original template. This preserves the template's layout and formatting.

2. **Hebrew Text Processing**:
   ```python
   def prepare_hebrew_text(self, text):
       reshaped_text = arabic_reshaper.reshape(str(text))
       bidi_text = get_display(reshaped_text)
       return bidi_text
   ```

3. **Font Selection Logic**:
   - Hebrew characters → Use registered Hebrew font (NotoSansHebrew)
   - ASCII only → Use Helvetica (better rendering for numbers)

4. **Signature Handling**:
   - Accepts base64-encoded PNG data URL
   - Scales image to fit signature area while preserving aspect ratio
   - Positioned at fixed coordinates on page 4

### 3. Field Mapping (`src/backend/field_mapping.py`)

**Role**: Define PDF coordinates for all form fields

**Structure**:
```python
FORM_FIELDS = {
    "field_name": {
        "x": int,           # X coordinate (points from left edge)
        "y": int,           # Y coordinate (points from bottom edge)
        "page": int,        # 0-indexed page number
        "max_length": int,  # Character limit
        "align": str,       # "left" or "right"
        "multiline": bool,  # Enable text wrapping
        "width": int,       # Max width for multiline (optional)
        "line_height": int, # Line spacing for multiline (optional)
        "checkbox": bool,   # Render as X mark (optional)
    }
}
```

**Field Categories** (by page):

| Page | Section | Field Count |
|------|---------|-------------|
| 0 | Visit Date | 3 |
| 0 | Employer Details | 12 |
| 0 | Worker Details | 14 |
| 0 | Previous Visits | 4 |
| 1 | Employer Assessment | 15 |
| 2 | Worker Report | 20 |
| 3 | Treatment Plan | 15 |

**Alignment Rules**:
- `align="right"` → Hebrew text (rendered right-to-left)
- `align="left"` → Numbers, emails, dates

### 4. PDF Validator (`src/backend/pdf_validator.py`)

**Role**: Validate uploaded PDFs match expected template structure

**Validation Checks**:
1. **Page count** - Must match template (4 pages)
2. **Page dimensions** - Must match within tolerance (5 points)
3. **Encryption** - PDF must not be password-protected
4. **Readability** - Can extract text from all pages

**Return Structure**:
```python
{
    "valid": bool,
    "errors": ["list of error messages"],  # Only if invalid
    "warnings": ["non-critical issues"],
    "info": {
        "page_count": int,
        "encrypted": bool,
        "has_form_fields": bool
    }
}
```

### 5. Frontend (`static/js/app.js`)

**Role**: Client-side form handling and API communication

**Key Features**:

1. **Form Data Collection**:
   ```javascript
   function collectFormData() {
       // Iterates through all form elements
       // Handles checkboxes, radio buttons, text inputs
       // Includes signature as base64 data URL
   }
   ```

2. **Signature Pad**:
   - Canvas-based drawing
   - Supports mouse and touch events
   - High DPI scaling for retina displays
   - Exports as PNG data URL

3. **PDF Upload Flow**:
   ```
   File Selected → Validate via API → Show Status → Enable Submit
   ```

4. **Auto-save** (optional, disabled by default):
   - Stores form data in localStorage
   - Survives page refresh

## Data Flow Diagrams

### Standard Form Submission
```
┌──────────┐     ┌─────────────┐     ┌──────────────┐
│  Browser │────>│ collectForm │────>│ POST /api/   │
│   Form   │     │    Data()   │     │    fill      │
└──────────┘     └─────────────┘     └──────────────┘
                                            │
                                            v
                                     ┌──────────────┐
                                     │  PDFFiller   │
                                     │ fill_form()  │
                                     └──────────────┘
                                            │
                        ┌───────────────────┼───────────────────┐
                        v                   v                   v
                ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
                │  Read Field  │   │ Create Blank │   │ Read Hebrew  │
                │  Mapping     │   │  Overlay PDF │   │    Font      │
                └──────────────┘   └──────────────┘   └──────────────┘
                        │                   │                   │
                        v                   v                   v
                ┌──────────────────────────────────────────────────┐
                │         For each field in form_data:             │
                │   - Look up coordinates from field_mapping       │
                │   - Process Hebrew text (bidi, reshape)          │
                │   - Draw on overlay canvas at (x, y)             │
                └──────────────────────────────────────────────────┘
                                            │
                                            v
                                     ┌──────────────┐
                                     │ Merge overlay│
                                     │ with template│
                                     └──────────────┘
                                            │
                                            v
                                     ┌──────────────┐
                                     │ Return PDF   │
                                     │   bytes      │
                                     └──────────────┘
```

### Uploaded PDF Flow
```
┌──────────┐     ┌──────────────┐     ┌───────────────┐
│ File     │────>│ validate-pdf │────>│ Page count?   │──No──> Error
│ Selected │     │   endpoint   │     │ Dimensions?   │
└──────────┘     └──────────────┘     │ Encrypted?    │
                                      └───────────────┘
                                            │ Yes
                                            v
                                     ┌──────────────┐
                                     │ Show "Valid" │
                                     │   status     │
                                     └──────────────┘
                                            │
                                      [User fills form]
                                            │
                                            v
┌──────────┐     ┌──────────────┐     ┌───────────────┐
│ Submit   │────>│ fill-uploaded│────>│PDFFillerFrom  │
│  Form    │     │   endpoint   │     │    Bytes()    │
└──────────┘     └──────────────┘     └───────────────┘
                                            │
                                     [Same as above]
                                            │
                                            v
                                     ┌──────────────┐
                                     │ Merge with   │
                                     │uploaded PDF  │
                                     └──────────────┘
```

## Key Design Decisions

### 1. Overlay vs. Form Field Editing

**Decision**: Use PDF overlay approach instead of editing AcroForm fields.

**Rationale**:
- Many government PDFs don't have proper form fields
- Overlay works with any PDF regardless of structure
- Preserves original PDF formatting exactly
- Simpler implementation

**Trade-offs**:
- Field positions must be manually mapped
- Changes to template PDF require coordinate updates

### 2. Stateless Architecture

**Decision**: No database, no sessions, no persistent storage.

**Rationale**:
- Simpler deployment
- No data privacy concerns
- Each request is independent
- Easy horizontal scaling

**Trade-offs**:
- Users must re-enter data if they close the page
- No submission history
- No user accounts

### 3. Hebrew Text Processing

**Decision**: Use python-bidi + arabic-reshaper for RTL text.

**Rationale**:
- Hebrew characters need bidirectional algorithm
- Some characters (like Arabic) need reshaping
- PDF canvas doesn't handle RTL natively

**Implementation**:
```python
# This transforms "שלום" to correct visual order for PDF
reshaped = arabic_reshaper.reshape(text)  # Handle character joining
visual = get_display(reshaped)            # Apply bidi algorithm
```

### 4. Font Strategy

**Decision**: Embed Hebrew font, fall back to system font.

**Rationale**:
- Deployment environments may not have Hebrew fonts
- System fonts work well for local development
- Noto Sans Hebrew has good coverage

**Font Priority**:
1. `fonts/NotoSansHebrew-Regular.ttf` (embedded)
2. `/Library/Fonts/Arial Unicode.ttf` (macOS)
3. Helvetica (fallback, no Hebrew support)

## Known Issues & Planned Fixes

### 1. Signature Placement - FIXED

**Status**: Resolved

**Solution Applied**: Modified `pdf_filler.py` to support dual signature placement:
- Changed `SIGNATURE_CONFIG` to `SIGNATURE_CONFIGS` list with two locations
- Updated `_draw_signature()` to accept config parameter
- Signature now renders at both y=420 (social worker area) and y=335 (bottom near visit date)

### 2. Checkbox Position Misalignment - FIXED

**Status**: Resolved

**Solution Applied**: All 24 checkbox fields in `field_mapping.py` have been updated with correct coordinates extracted from the template PDF using `tools/find_checkbox_positions.py`. The X marks now align properly within their respective checkbox boxes.

**Verification**: Run `python tools/test_coordinates.py` to generate a test PDF with all checkboxes marked, then visually verify alignment.

### 3. Text Field Position Audit

**Status**: Pending

**Issue**: Text field coordinates in `field_mapping.py` may be misaligned with the template PDF. While checkboxes have been fixed, text fields need verification.

**Fix Required**:
1. Generate comprehensive test PDF with all fields populated
2. Compare each field's output position against template
3. Adjust x/y coordinates in `field_mapping.py` as needed

**Fields to verify** (80+ fields across 4 pages):
- Page 1: Visit date, employer details, worker details, placement info
- Page 2: Employer assessment fields (multiline text areas)
- Page 3: Worker report fields, contract details, payment info
- Page 4: Treatment plan, summary fields, signature section

### 4. Date Field Constraints - FIXED

**Status**: Resolved

**Solution Applied**: Converted all date fields to native HTML5 `type="date"` inputs:
- Visit date, placement dates, insurance dates, signature date
- JavaScript converts YYYY-MM-DD to DD/MM/YYYY format for PDF
- Visit date is split into day/month/year components for PDF fields
- Mobile devices show native date picker for excellent UX
- Added CSS styling for touch-friendly date inputs (min-height: 52px on mobile)

### 4. UX/UI Improvements Needed

**Current State**: Functional but basic styling.

**Required Improvements**:

| Area | Current | Target |
|------|---------|--------|
| Visual design | Basic CSS | Modern, professional look |
| Mobile experience | Responsive but cramped | Touch-optimized, spacious |
| Form navigation | Single long scroll | Section-based with progress |
| User feedback | Minimal | Clear status, validation hints |
| Accessibility | Basic RTL | Full a11y compliance |

**Technical Approach**:
- Keep vanilla CSS/JS (no framework dependencies)
- Use CSS Grid/Flexbox for layout
- Add CSS custom properties for theming
- Implement collapsible form sections
- Add smooth scroll and transitions

## Adding New Form Types

To support a different PDF form:

1. **Create field mapping file**:
   ```python
   # src/backend/new_form_mapping.py
   FORM_FIELDS = {
       # Map all fields with coordinates
   }
   ```

2. **Add template PDF**:
   - Place in `templates/new_form_template.pdf`

3. **Create HTML form**:
   - Add `templates/new_form.html`

4. **Add API routes**:
   ```python
   @app.route('/new-form')
   def new_form():
       return render_template('new_form.html')

   @app.route('/api/fill-new-form', methods=['POST'])
   def fill_new_form():
       # Similar to existing fill_form
   ```

## Performance Considerations

### Current Performance
- PDF generation: ~200-500ms per form
- Most time spent in PDF merge operation
- Font loading is cached after first use

### Optimization Opportunities
- Pre-load template PDF on startup
- Cache font objects
- Use async workers for high load
- Consider PDF streaming for large files

## Security Considerations

### Current Security Model
- No authentication (public access)
- No input validation beyond length limits
- File uploads limited to 16MB
- PDF files not scanned for malware

### Recommendations for Production
1. Add authentication layer
2. Implement rate limiting
3. Add input sanitization
4. Scan uploaded PDFs
5. Use HTTPS
6. Add CSRF protection

## Testing Strategy

### Manual Testing
```bash
# Test coordinate positioning
python test_coordinates.py

# Check generated PDF
open test_output.pdf
```

### Areas Needing Tests
- Unit tests for field_mapping validation
- Integration tests for API endpoints
- End-to-end tests for form submission
- Visual regression tests for PDF output

## Monitoring and Debugging

### Logging
- Flask logs all requests to stdout
- PDF errors logged with traceback
- Font loading status logged on startup

### Debug Mode
```bash
# Enable Flask debug mode
FLASK_ENV=development python app.py
```

### Common Debug Points
- `pdf_filler.py:126` - Field drawing
- `pdf_filler.py:214` - Signature embedding
- `app.py:81` - Form data processing

## Dependencies

### Critical Dependencies
| Package | Version | Purpose | Alternative |
|---------|---------|---------|-------------|
| Flask | 3.1.0 | Web framework | FastAPI, Django |
| pypdf | 6.6.2 | PDF reading/merging | PyPDF2 (legacy) |
| reportlab | 4.2.5 | PDF generation | None |
| python-bidi | 0.4.2 | RTL text | None |
| arabic-reshaper | 3.0.0 | Text shaping | None |

### Optional Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| gunicorn | 23.0.0 | Production WSGI server |
| pdfplumber | 0.11.9 | PDF analysis (dev only) |

## Version History

### v1.0 (Current)
- Initial production release
- Full form support (4 pages, 80+ fields)
- Hebrew RTL text support
- Signature drawing
- PDF upload and validation
- PWA manifest

---

*For general usage information, see [README.md](README.md)*
