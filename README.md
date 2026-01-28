# PDF Form Filler

A web application for digitally filling out Hebrew PDF forms, specifically designed for the "Regular Visit" (ביקור רגיל) form used in elderly care services documentation in Israel.

## Purpose

Social workers in Israel need to complete standardized PDF forms during home visits to elderly clients with foreign caregivers. This application:

- **Eliminates manual PDF filling** - Replace handwriting with a clean web interface
- **Supports Hebrew RTL text** - Proper right-to-left rendering in PDFs
- **Works offline-ready** - PWA-capable for use in the field
- **Preserves privacy** - Stateless design with no data storage

## Current State

**Version**: 1.0 (Production-ready)

### Implemented Features

| Feature | Status | Description |
|---------|--------|-------------|
| Web Form Interface | Done | Full 4-page form with all fields |
| Hebrew RTL Support | Done | BiDi algorithm + text reshaping |
| PDF Generation | Done | Coordinate-based overlay on template |
| Signature Drawing | Done | Canvas-based signature capture |
| PDF Upload | Done | Use pre-filled PDFs as base |
| PDF Validation | Done | Structure verification before processing |
| Mobile Support | Done | Touch-friendly, responsive design |
| PWA Manifest | Done | Installable as mobile app |

### Known Limitations

- Single form template (Regular Visit only)
- No form data persistence between sessions
- No user authentication
- No multi-user collaboration

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Browser                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              HTML Form (form.html)                   │    │
│  │  - RTL Hebrew interface                              │    │
│  │  - Signature canvas                                  │    │
│  │  - PDF upload with validation                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              JavaScript (app.js)                     │    │
│  │  - Form data collection                              │    │
│  │  - Signature capture (touch/mouse)                   │    │
│  │  - API communication                                 │    │
│  │  - File download handling                            │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                      HTTP/JSON
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Flask Server (app.py)                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  API Endpoints                       │    │
│  │  GET  /           → Serve form page                  │    │
│  │  POST /api/fill   → Fill template PDF                │    │
│  │  POST /api/fill-uploaded → Fill uploaded PDF         │    │
│  │  POST /api/validate-pdf  → Validate PDF structure    │    │
│  │  GET  /api/fields → List available fields            │    │
│  │  GET  /health     → Health check                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              PDF Processing Module                   │    │
│  │  ┌──────────────────┐  ┌──────────────────────┐     │    │
│  │  │  pdf_filler.py   │  │  field_mapping.py    │     │    │
│  │  │  - PDF overlay   │  │  - Field coordinates │     │    │
│  │  │  - Text render   │  │  - 80+ field defs    │     │    │
│  │  │  - Hebrew BiDi   │  │  - Checkbox support  │     │    │
│  │  │  - Signature img │  │  - Multiline config  │     │    │
│  │  └──────────────────┘  └──────────────────────────┘     │    │
│  │  ┌──────────────────┐                                │    │
│  │  │ pdf_validator.py │                                │    │
│  │  │ - Page count     │                                │    │
│  │  │ - Size matching  │                                │    │
│  │  │ - Encryption chk │                                │    │
│  │  └──────────────────┘                                │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. User fills form in browser
2. JavaScript collects form data + signature as JSON
3. POST to `/api/fill` or `/api/fill-uploaded`
4. Server creates transparent overlay PDF with data
5. Overlay merged with template PDF
6. Filled PDF returned as download

### PDF Coordinate System

```
PDF Page (A4: 595.3 x 841.9 points)
┌─────────────────────────────────────┐ y=841.9
│                                     │
│  Hebrew text uses align="right"     │
│  Numbers use align="left"           │
│                                     │
│  x increases →                      │
│  y increases ↑                      │
│                                     │
(0,0)─────────────────────────────────┘ y=0
x=0                               x=595.3
```

## Technology Stack

### Backend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Web Framework | Flask 3.1 | HTTP server, routing, templates |
| PDF Reading | pypdf 6.6 | Parse and merge PDF files |
| PDF Generation | ReportLab 4.2 | Create overlay with text/images |
| PDF Analysis | pdfplumber 0.11 | Extract text positions (dev tool) |
| Hebrew Text | python-bidi + arabic-reshaper | RTL text rendering |
| Production Server | Gunicorn 23 | WSGI server for deployment |

### Frontend
| Component | Technology | Purpose |
|-----------|------------|---------|
| Markup | HTML5 | Semantic form structure |
| Styling | CSS3 | RTL layout, responsive design |
| Logic | Vanilla JavaScript | Form handling, signature canvas |
| PWA | Web App Manifest | Mobile installation |

### Fonts
- **NotoSansHebrew** - Embedded TTF for server deployment
- **Arial Unicode** - System fallback for local development

## Project Structure

```
formFiller/
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── src/
│   └── backend/
│       ├── __init__.py
│       ├── pdf_filler.py       # Core PDF generation logic
│       ├── field_mapping.py    # PDF coordinate definitions (80+ fields)
│       └── pdf_validator.py    # Uploaded PDF validation
│
├── templates/
│   ├── template.pdf            # Original PDF form template
│   └── form.html               # Web form interface (Jinja2)
│
├── static/
│   ├── css/
│   │   └── style.css           # Form styling, RTL support
│   ├── js/
│   │   └── app.js              # Client-side form logic
│   └── manifest.json           # PWA manifest
│
├── fonts/
│   └── NotoSansHebrew-Regular.ttf  # Embedded Hebrew font
│
├── tools/
│   └── analyze_pdf.py          # PDF field analysis utility
│
└── venv/                       # Python virtual environment
```

## Installation

### Prerequisites
- Python 3.10+
- pip package manager

### Setup

```bash
# Clone repository
git clone <repository-url>
cd formFiller

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify template PDF exists
ls templates/template.pdf
```

### Font Setup

The application includes an embedded Hebrew font (`fonts/NotoSansHebrew-Regular.ttf`). On macOS with Arial Unicode installed, it will use that as a fallback.

## Usage

### Running Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python app.py

# Open browser
open http://localhost:5001
```

### Filling a Form

1. Navigate to the web interface
2. Optionally upload a pre-filled PDF
3. Complete the form fields
4. Draw signature in the signature pad
5. Click "הפק PDF" to generate and download

### Using Pre-filled PDFs

Users can upload PDFs that already have some fields filled (e.g., employer/worker details from CRM systems):

1. Click "בחר קובץ" in the upload section
2. Select a 4-page PDF matching the template structure
3. Wait for validation (green checkmark)
4. Fill remaining fields
5. Generate the final PDF

## API Reference

### `GET /`
Serves the main form interface.

### `POST /api/fill`
Fill the template PDF with form data.

**Request:**
```json
{
  "employer_first_name": "ישראל",
  "employer_last_name": "ישראלי",
  "employer_id": "123456789",
  "visit_date_day": "15",
  "visit_date_month": "01",
  "visit_date_year": "2025",
  "signature_image": "data:image/png;base64,..."
}
```

**Response:** PDF file (application/pdf)

### `POST /api/fill-uploaded`
Fill an uploaded PDF with form data.

**Request:** `multipart/form-data`
- `pdf_file`: The uploaded PDF file
- `form_data`: JSON string of form fields

**Response:** PDF file (application/pdf)

### `POST /api/validate-pdf`
Validate an uploaded PDF structure.

**Request:** `multipart/form-data`
- `pdf_file`: The PDF to validate

**Response:**
```json
{
  "valid": true,
  "warnings": ["PDF contains form fields - they will be preserved but not used"],
  "info": {
    "page_count": 4,
    "encrypted": false,
    "has_form_fields": true
  }
}
```

### `GET /api/fields`
List all available form fields with metadata.

**Response:**
```json
{
  "employer_first_name": {
    "type": "text",
    "multiline": false,
    "max_length": 20,
    "page": 0
  }
}
```

### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "template_exists": true
}
```

## Development Guide

### Adding New Fields

1. **Analyze the PDF** to find field coordinates:
   ```bash
   python tools/analyze_pdf.py
   ```

2. **Add field definition** to `src/backend/field_mapping.py`:
   ```python
   "new_field_name": {
       "x": 300,           # X coordinate (points from left)
       "y": 500,           # Y coordinate (points from bottom)
       "page": 0,          # Page number (0-indexed)
       "max_length": 50,   # Maximum characters
       "align": "right",   # "right" for Hebrew, "left" for numbers
       "multiline": False  # True for textarea fields
   }
   ```

3. **Add HTML input** to `templates/form.html`:
   ```html
   <div class="form-group">
       <label for="new_field_name">תווית השדה</label>
       <input type="text" id="new_field_name" name="new_field_name" maxlength="50">
   </div>
   ```

4. **Test** the field positioning:
   ```bash
   python test_coordinates.py
   ```

### Field Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `x` | int | X coordinate in PDF points |
| `y` | int | Y coordinate in PDF points |
| `page` | int | Page number (0-indexed) |
| `max_length` | int | Maximum character limit |
| `align` | string | "left" or "right" |
| `multiline` | bool | Enable text wrapping |
| `width` | int | Max width for multiline (points) |
| `line_height` | int | Line spacing for multiline |
| `checkbox` | bool | Render as checkbox (X mark) |

### Coordinate Tips

- PDF coordinates start from **bottom-left corner**
- 72 points = 1 inch
- A4 page: 595.27 x 841.89 points
- Use `align="right"` for Hebrew text
- Use `align="left"` for numbers, emails, dates

## Deployment

### Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
```

```bash
docker build -t pdf-form-filler .
docker run -p 5001:5001 pdf-form-filler
```

### Cloud Platforms

| Platform | Deployment Method |
|----------|-------------------|
| AWS | EC2, ECS, or Lambda (with Zappa) |
| Azure | App Service or Container Instances |
| Google Cloud | Cloud Run or App Engine |
| Heroku | Git push deployment |
| Railway | Git integration |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 5001 | Server port |
| `FLASK_ENV` | production | Flask environment |

## Troubleshooting

### Hebrew text appears reversed
- Ensure `python-bidi` and `arabic-reshaper` are installed
- Check that text is processed through `prepare_hebrew_text()`

### PDF fields are misaligned
1. Adjust coordinates in `field_mapping.py`
2. Run `python test_coordinates.py`
3. Check output PDF positioning
4. Iterate until correct

### Font not rendering
- Check `fonts/NotoSansHebrew-Regular.ttf` exists
- On macOS, verify Arial Unicode is installed
- Check console for font registration errors

### Upload validation fails
- Ensure PDF has exactly 4 pages
- Check page dimensions match template
- PDF must not be password-protected

### Form submission fails
- Check browser console for JavaScript errors
- Verify Flask server is running
- Check server logs for Python exceptions

## Future Enhancements

### High Priority (Next Release)

- [ ] **Dual signature placement** - Place the drawn signature in both the social worker signature field AND the general signature field at the bottom of page 4
- [x] **Fix checkbox positions** - Correct the X/Y coordinates of checkbox marks in the output PDF to align properly with the template
- [ ] **Improved date inputs** - Add constrained date fields with date pickers or DD/MM/YYYY masks to prevent invalid date entry
- [ ] **UX/UI makeover** - Complete redesign of the form interface for both desktop and mobile:
  - Modern, clean visual design
  - Improved mobile touch experience
  - Better form section organization
  - Progress indicator for multi-section form
  - Smooth transitions and feedback
  - Accessible color scheme and typography

### Planned Features

- [ ] **Multi-template support** - Support for different form types
- [ ] **Form data persistence** - Save/load form drafts
- [ ] **User authentication** - Secure access control
- [ ] **Database integration** - Store submission history
- [ ] **Email delivery** - Send PDFs directly via email
- [ ] **Batch processing** - Fill multiple forms at once
- [ ] **Field validation** - Client and server-side validation
- [ ] **Auto-fill from CRM** - API integration with social services systems
- [ ] **Offline mode** - Full PWA with service worker caching
- [ ] **Audit logging** - Track form generations

### Technical Improvements

- [ ] Form field position visual mapper tool
- [ ] Automated coordinate extraction from PDFs
- [ ] Unit and integration tests
- [ ] CI/CD pipeline
- [ ] TypeScript migration for frontend
- [ ] React/Vue frontend option

## License

Proprietary - Internal use only

## Support

For issues or questions, contact the development team or open an issue in the repository.

---

*Last updated: January 2025*
