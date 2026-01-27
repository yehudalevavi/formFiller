#!/usr/bin/env python3
"""
Deeper analysis of PDF structure
"""
import pdfplumber
from pypdf import PdfReader

def analyze_pdf_detailed(pdf_path):
    """Analyze PDF structure in detail"""
    print(f"Analyzing: {pdf_path}\n")
    print("="*80)

    # Check with pypdf for annotations
    print("\n1. Checking for Annotations and Interactive Elements:")
    reader = PdfReader(pdf_path)
    for i, page in enumerate(reader.pages):
        print(f"\nPage {i+1}:")
        if '/Annots' in page:
            annots = page['/Annots']
            print(f"  Found {len(annots)} annotations")
            for j, annot in enumerate(annots):
                annot_obj = annot.get_object()
                print(f"    Annotation {j+1}:")
                print(f"      Type: {annot_obj.get('/Subtype', 'Unknown')}")
                if '/T' in annot_obj:  # Field name
                    print(f"      Field Name: {annot_obj['/T']}")
                if '/FT' in annot_obj:  # Field type
                    print(f"      Field Type: {annot_obj['/FT']}")
        else:
            print("  No annotations found")

    # Check text content and layout
    print("\n" + "="*80)
    print("\n2. Text Content Analysis:")
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            print(f"\nPage {i+1}:")
            text = page.extract_text()
            if text:
                lines = text.split('\n')[:20]  # First 20 lines
                print(f"  First {len(lines)} lines of text:")
                for line in lines:
                    print(f"    {line}")
            else:
                print("  No text extracted")

            # Check for tables
            tables = page.extract_tables()
            if tables:
                print(f"  Found {len(tables)} table(s)")

if __name__ == "__main__":
    pdf_path = "/Users/ylevavi/Downloads/ביקור רגיל ליהודה (1).pdf"
    analyze_pdf_detailed(pdf_path)
