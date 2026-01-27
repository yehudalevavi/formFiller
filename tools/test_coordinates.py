#!/usr/bin/env python3
"""
Test script to verify PDF coordinate mapping
Creates a test PDF with sample data to verify field positions
"""
import sys
sys.path.insert(0, 'src')

from backend.pdf_filler import fill_pdf_form

# Test data - only fields that need to be filled (pre-filled fields excluded)
test_data = {
    # Page 1 - Visit Date
    "visit_date_day": "27",
    "visit_date_month": "01",
    "visit_date_year": "2026",

    # Page 2 - Employer Assessment
    "appearance_description": "רגוע, נקי, לבוש בהתאם לעונה",
    "nutritional_status": "נראה בהתאם לגילו",
    "external_signs": "ללא סימנים חריגים",
    "functional_status": "עצמאי, זקוק לעזרה במעברים",
    "health_status": "תקין, סוכרת מאוזנת",
    "was_hospitalized_no": True,
    "cognitive_description": "תקשורת תקינה, זיכרון תקין",
    "home_maintenance": "הבית נקי ומסודר",
    "food_supply": "בן המשפחה קונה, ארוחות מסופקות",
    "client_satisfaction": "מרוצה מאוד",
    "family_satisfaction": "מרוצה",
    "service_difficulties": "אין קשיים",
    "special_requests": "אין בקשות מיוחדות",

    # Page 3 - Worker Report
    "worker_appearance": "מסודרת ונקייה",
    "worker_training": "כן, קיבלה הדרכה מלאה",
    "worker_duties": "ניקיון, כביסה, בישול, ליווי לטיפולים",
    "worker_satisfaction": "מרוצה",
    "work_difficulties": "לא נצפו קשיים",
    "duties_match_satisfaction": "כן, יש התאמה",
    "worker_has_friends": "כן",

    "contract_employer": True,
    "contract_translated_yes": True,
    "insurance_from": "01/01/2026",
    "insurance_to": "31/12/2026",
    "insurance_company": "הראל",
    "last_insurance_payment": "01/01/2026",
    "monthly_salary": "6000",
    "total_payment": "6500",
    "payment_date": "1",
    "payment_bank": True,
    "weekly_day_off": "שבת",
    "accommodation": "חדר פרטי עם מזגן",
    "notes": "הכל תקין",

    # Page 4 - Treatment Plan
    "treatment_essence": "המשך מעקב שוטף",
    "treatment_followup": True,
    "summary_employer": "מצב הקשיש טוב, מרוצה מהטיפול",
    "summary_caregiver": "העובדת מרוצה ומבצעת עבודתה היטב",

    "attendee_employer": True,
    "attendee_worker": True,

    "signer_id": "123456789",
    "social_worker_name_signature": "ישראל ישראלי",
    "responsible_worker_name": "דנה כהן",
    "responsible_worker_id": "987654321",
    "signature_date": "27/01/2026",
}

if __name__ == "__main__":
    template_path = "templates/template.pdf"
    output_path = "test_output.pdf"

    print("Filling PDF form with test data...")

    try:
        fill_pdf_form(template_path, test_data, output_path)
        print(f"Success! Test PDF created at: {output_path}")
        print("Please open the file and verify field positions.")

        # Open the file
        import os
        os.system(f"open {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
