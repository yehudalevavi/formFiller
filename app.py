#!/usr/bin/env python3
"""
Flask application for PDF form filling
"""
import os
import json
from flask import Flask, render_template, request, send_file, jsonify
from io import BytesIO
from datetime import datetime
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.pdf_filler import fill_pdf_form, fill_pdf_from_bytes
from backend.pdf_validator import validate_uploaded_pdf
from backend.field_mapping import FORM_FIELDS

app = Flask(__name__)
app.config['TEMPLATES_FOLDER'] = 'templates'
app.config['TEMPLATE_PDF'] = os.path.join('templates', 'template.pdf')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


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


@app.route('/api/fill-uploaded', methods=['POST'])
def fill_uploaded_form():
    """Fill an uploaded PDF form with submitted data"""
    try:
        # Check if file was uploaded
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'}), 400

        pdf_file = request.files['pdf_file']

        if pdf_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'File must be a PDF'}), 400

        # Get form data from the request
        form_data_json = request.form.get('form_data')
        if not form_data_json:
            return jsonify({'error': 'No form data provided'}), 400

        try:
            form_data = json.loads(form_data_json)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid form data format'}), 400

        # Read the uploaded PDF
        pdf_bytes = pdf_file.read()

        # Validate the uploaded PDF structure
        validation_result = validate_uploaded_pdf(
            pdf_bytes,
            app.config['TEMPLATE_PDF']
        )

        if not validation_result['valid']:
            return jsonify({
                'error': 'PDF validation failed',
                'details': validation_result['errors']
            }), 400

        # Fill the uploaded PDF with form data
        filled_pdf_bytes = fill_pdf_from_bytes(pdf_bytes, form_data)

        # Create response
        pdf_output = BytesIO(filled_pdf_bytes)
        pdf_output.seek(0)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'visit_report_{timestamp}.pdf'

        return send_file(
            pdf_output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        app.logger.error(f"Error filling uploaded form: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate-pdf', methods=['POST'])
def validate_pdf():
    """Validate an uploaded PDF without filling it"""
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'}), 400

        pdf_file = request.files['pdf_file']

        if pdf_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'File must be a PDF'}), 400

        pdf_bytes = pdf_file.read()

        validation_result = validate_uploaded_pdf(
            pdf_bytes,
            app.config['TEMPLATE_PDF']
        )

        return jsonify(validation_result)

    except Exception as e:
        app.logger.error(f"Error validating PDF: {str(e)}")
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
