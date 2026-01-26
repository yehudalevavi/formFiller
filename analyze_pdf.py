#!/usr/bin/env python3
"""
Script to analyze PDF form fields
"""
import sys

try:
    from pypdf import PdfReader
except ImportError:
    print("pypdf not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
    from pypdf import PdfReader

def analyze_pdf_form(pdf_path):
    """Extract and display all form fields from a PDF"""
    reader = PdfReader(pdf_path)

    print(f"PDF Analysis for: {pdf_path}")
    print(f"Number of pages: {len(reader.pages)}")
    print("\n" + "="*80)

    # Get form fields
    if reader.get_fields() is None:
        print("No form fields found in this PDF")
        return

    fields = reader.get_fields()
    print(f"\nTotal form fields found: {len(fields)}")
    print("\n" + "="*80)
    print("\nField Details:\n")

    for field_name, field_info in fields.items():
        print(f"Field Name: {field_name}")
        print(f"  Field Type: {field_info.get('/FT', 'Unknown')}")
        print(f"  Field Value: {field_info.get('/V', 'Empty')}")
        print(f"  Field Flags: {field_info.get('/Ff', 'None')}")

        # Check for options (for dropdowns, radio buttons)
        if '/Opt' in field_info:
            print(f"  Options: {field_info['/Opt']}")

        # Check for default value
        if '/DV' in field_info:
            print(f"  Default Value: {field_info['/DV']}")

        print()

    return fields

if __name__ == "__main__":
    pdf_path = "/Users/ylevavi/Downloads/ביקור רגיל ליהודה (1).pdf"
    analyze_pdf_form(pdf_path)
