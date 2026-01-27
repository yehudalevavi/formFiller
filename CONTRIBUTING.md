# Contributing Guide

Quick reference for developers and AI agents working on this project.

## Quick Start

```bash
# Setup
cd formFiller
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python app.py
# Open http://localhost:5001
```

## Common Tasks

### Adding a New Field

1. Find coordinates using PDF analysis:
   ```bash
   python tools/analyze_pdf.py
   ```

2. Add to `src/backend/field_mapping.py`:
   ```python
   "field_name": {"x": 300, "y": 500, "page": 0, "max_length": 50, "align": "right"}
   ```

3. Add to `templates/form.html`:
   ```html
   <input type="text" name="field_name" id="field_name" maxlength="50">
   ```

4. Test: `python test_coordinates.py`

### Adjusting Field Position

1. Open `src/backend/field_mapping.py`
2. Find the field by name
3. Adjust `x` (horizontal) or `y` (vertical) values
4. Test: `python test_coordinates.py`
5. Check `test_output.pdf`

### Adding a Checkbox

```python
"checkbox_name": {"x": 100, "y": 200, "page": 0, "checkbox": True}
```

In HTML:
```html
<input type="checkbox" name="checkbox_name">
```

### Adding a Multiline Field

```python
"field_name": {
    "x": 545,
    "y": 500,
    "page": 1,
    "max_length": 300,
    "multiline": True,
    "width": 490,
    "line_height": 12,
    "align": "right"
}
```

## File Locations

| Task | File |
|------|------|
| Change field positions | `src/backend/field_mapping.py` |
| Modify form HTML | `templates/form.html` |
| Change styling | `static/css/style.css` |
| Modify JavaScript | `static/js/app.js` |
| Change PDF logic | `src/backend/pdf_filler.py` |
| Add API endpoints | `app.py` |

## Coordinate Tips

- PDF origin is **bottom-left**
- Hebrew text: use `align="right"`, x = where text **ends**
- Numbers/email: use `align="left"`, x = where text **starts**
- Page 0 = first page, Page 3 = fourth page
- 72 points = 1 inch

## Testing Changes

```bash
# Test PDF generation
python test_coordinates.py
open test_output.pdf

# Test server
python app.py
# Fill form at http://localhost:5001
```

## Code Style

- Python: Follow PEP 8
- JavaScript: Use vanilla JS (no frameworks)
- HTML: Use semantic elements
- Comments: Only where logic isn't obvious

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/description

# Make changes, then commit
git add <specific-files>
git commit -m "Add feature: description"

# Push and create PR
git push origin feature/description
```
