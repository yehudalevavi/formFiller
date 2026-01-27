#!/usr/bin/env python3
"""
Flask application for PDF form filling
"""
import os
from flask import Flask, render_template, request, send_file, jsonify
from io import BytesIO
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.pdf_filler import fill_pdf_form
from backend.field_mapping import FORM_FIELDS

app = Flask(__name__)
app.config['TEMPLATES_FOLDER'] = 'templates'
app.config['TEMPLATE_PDF'] = os.path.join('templates', 'template.pdf')


@app.route('/')
def index():
    """Render the main form page"""
    return render_template('form.html')


@app.route('/api/fields', methods=['GET'])
def get_fields():
    """Return list of all form fields"""
    fields_info = {}
    for field_name, field_config in FORM_FIELDS.items():
        fields_info[field_name] = {
            'type': 'checkbox' if field_config.get('checkbox') else 'text',
            'multiline': field_config.get('multiline', False),
            'max_length': field_config.get('max_length'),
            'page': field_config.get('page')
        }
    return jsonify(fields_info)


@app.route('/api/fill', methods=['POST'])
def fill_form():
    """Fill the PDF form with submitted data"""
    try:
        # Get form data from request
        form_data = request.get_json()

        if not form_data:
            return jsonify({'error': 'No form data provided'}), 400

        # Validate template exists
        if not os.path.exists(app.config['TEMPLATE_PDF']):
            return jsonify({'error': 'Template PDF not found'}), 500

        # Fill the PDF
        pdf_bytes = fill_pdf_form(
            app.config['TEMPLATE_PDF'],
            form_data,
            output_path=None
        )

        # Create response
        pdf_file = BytesIO(pdf_bytes)
        pdf_file.seek(0)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'visit_report_{timestamp}.pdf'

        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        app.logger.error(f"Error filling form: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'template_exists': os.path.exists(app.config['TEMPLATE_PDF'])
    })


if __name__ == '__main__':
    # Check template exists
    if not os.path.exists(app.config['TEMPLATE_PDF']):
        print(f"Warning: Template PDF not found at {app.config['TEMPLATE_PDF']}")

    port = 5001
    print("Starting PDF Form Filler application...")
    print(f"Navigate to http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
