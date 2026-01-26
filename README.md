# PDF Form Filler - Regular Visit Form

A web application for filling out the "Regular Visit" (ביקור רגיל) PDF form digitally, specifically designed for elderly care services documentation.

## Features

- **Hebrew RTL Support**: Full right-to-left language support
- **User-Friendly Interface**: Clean, modern web form replacing manual PDF filling
- **Coordinate-Based PDF Filling**: Overlays data onto existing PDF template
- **Stateless Design**: No data storage - fill and download
- **Responsive Design**: Works on desktop and mobile devices
- **Local or Cloud Ready**: Run locally or deploy to cloud services

## Technology Stack

- **Backend**: Python 3, Flask
- **PDF Processing**: pypdf, reportlab, pdfplumber
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Hebrew Text**: python-bidi, arabic-reshaper for proper RTL display

## Project Structure

```
formFiller/
├── app.py                      # Flask application entry point
├── requirements.txt            # Python dependencies
├── src/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── pdf_filler.py      # PDF filling logic
│   │   └── field_mapping.py   # Coordinate mappings for PDF fields
│   └── frontend/
├── templates/
│   ├── template.pdf           # Original PDF template
│   └── form.html             # Web form interface
├── static/
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── app.js            # Client-side logic
├── venv/                      # Python virtual environment
├── test_coordinates.py        # Test script for coordinate verification
└── analyze_pdf*.py           # PDF analysis utilities

```

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure template PDF exists**:
   - Place your PDF template at `templates/template.pdf`

## Usage

### Running Locally

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Fill out the form** with all required information

4. **Click "הפק PDF"** to generate and download the filled PDF

### Testing

To test the PDF coordinate mapping with sample data:

```bash
python test_coordinates.py
```

This will create `test_output.pdf` with sample data to verify field positioning.

## Coordinate Adjustment

If PDF fields are not aligned correctly:

1. Open `src/backend/field_mapping.py`
2. Adjust the `x` and `y` coordinates for each field
3. Run `python test_coordinates.py` to verify changes
4. Iterate until fields are correctly positioned

### Understanding Coordinates

- PDF coordinates start from **bottom-left corner**
- Units are in **points** (72 points = 1 inch)
- Standard A4 page: 595.27 x 841.89 points
- For Hebrew RTL text, position from the right side

## API Endpoints

### `GET /`
Returns the main form interface

### `POST /api/fill`
Fills the PDF with submitted data

**Request Body** (JSON):
```json
{
  "visit_date_day": "15",
  "visit_date_month": "01",
  "visit_date_year": "2025",
  "office_name": "משרד רווחה תל אביב",
  ...
}
```

**Response**: PDF file download

### `GET /api/fields`
Returns list of all available form fields with metadata

### `GET /health`
Health check endpoint

## Development

### Adding New Fields

1. Add field definition to `src/backend/field_mapping.py`:
   ```python
   "field_name": {"x": 100, "y": 200, "page": 0, "max_length": 50}
   ```

2. Add corresponding input to `templates/form.html`:
   ```html
   <input type="text" name="field_name" id="field_name">
   ```

3. Test with `test_coordinates.py`

### Git Workflow for Feature Branches

Since you're using git worktrees:

```bash
# Create a new feature branch
git worktree add ../formfiller-feature-name feature-name

# Work in the new worktree
cd ../formfiller-feature-name

# When done, commit and push
git add .
git commit -m "Add feature"
git push origin feature-name

# Merge back to main when ready
```

## Deployment

### Docker (Recommended for Cloud)

Create a `Dockerfile`:
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t pdf-form-filler .
docker run -p 5000:5000 pdf-form-filler
```

### Cloud Platforms

- **AWS**: Deploy on EC2, ECS, or Lambda
- **Azure**: App Service or Container Instances
- **Google Cloud**: Cloud Run or App Engine
- **Heroku**: Direct git deployment

## Troubleshooting

### Hebrew text appears reversed or broken
- Ensure `python-bidi` and `arabic-reshaper` are installed
- Check that `prepare_hebrew_text()` is being called

### PDF fields are misaligned
- Adjust coordinates in `field_mapping.py`
- Test with `test_coordinates.py`
- Open test output in PDF viewer to verify positions

### Form submission fails
- Check browser console for JavaScript errors
- Verify Flask server is running
- Check server logs for Python errors

## Future Enhancements

- [ ] Database integration for saving submissions
- [ ] User authentication
- [ ] Multiple form templates support
- [ ] Email PDF delivery
- [ ] Form validation
- [ ] Multi-page form with progress indicator
- [ ] PDF field position visual mapper tool

## License

Proprietary - Internal use only

## Support

For issues or questions, contact the development team.
