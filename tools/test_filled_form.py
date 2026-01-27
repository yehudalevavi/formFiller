#!/usr/bin/env python3
"""
Test script to fill PDF with comprehensive sample data and verify positions
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from backend.pdf_filler import fill_pdf_form

# Comprehensive test data in Hebrew
test_data = {
    # Page 1 - Visit details
    "visit_date_day": "27",
    "visit_date_month": "01",
    "visit_date_year": "2025",

    # Employer details
    "employer_last_name": "כהן",
    "employer_first_name": "דוד",
    "employer_id": "123456789",

    # Employer address
    "employer_street": "הרצל",
    "employer_house_number": "42",
    "employer_entrance": "א",
    "employer_apartment": "5",
    "employer_city": "תל אביב",
    "employer_zipcode": "6100000",

    # Employer contact
    "employer_landline": "03-1234567",
    "employer_mobile": "054-1234567",
    "employer_email": "david@example.com",

    # Worker details
    "worker_passport": "AB1234567",
    "worker_last_name": "גרסיה",
    "worker_first_name": "מריה",
    "worker_origin_country": "פיליפינים",
    "worker_mobile": "050-9876543",

    # Placement
    "placement_start_date": "01/01/2024",
    "placement_israel": True,
    "placement_agency": "כח אדם בע\"מ",

    # Worker address
    "worker_street": "דיזנגוף",
    "worker_house_number": "100",
    "worker_entrance": "ב",
    "worker_apartment": "3",
    "worker_city": "תל אביב",
    "worker_day_off": "שישי",

    # Previous visits
    "pre_placement_date": "15/12/2023",
    "pre_placement_social_worker": "יעל לוי",
    "post_placement_date": "01/02/2024",
    "post_placement_social_worker": "רחל כהן",

    # Page 2 - Employer assessment
    "appearance_description": "מראה מטופח ונקי",
    "nutritional_status": "תזונה תקינה",
    "external_signs": "ללא סימנים חריגים",
    "functional_status": "עצמאי ברובו",
    "health_status": "מצב בריאותי טוב",
    "was_hospitalized_no": True,
    "cognitive_description": "תפקוד קוגניטיבי תקין",
    "home_maintenance": "הבית מתוחזק היטב",
    "food_supply": "יש אספקת מזון סדירה",
    "client_satisfaction": "מרוצה מאוד",
    "family_satisfaction": "המשפחה מרוצה",
    "service_difficulties": "אין קשיים מיוחדים",
    "special_requests": "אין בקשות מיוחדות",

    # Page 3 - Worker report
    "worker_appearance": "מראה מסודר ונקי",
    "worker_training": "קיבלה הדרכה מקיפה",
    "worker_duties": "טיפול בקשיש, עזרה בבית, בישול",
    "worker_satisfaction": "מרוצה מהעבודה",
    "work_difficulties": "ללא קשיים",
    "duties_match_satisfaction": "יש התאמה מלאה",
    "worker_has_friends": "יש חברים באזור",

    "contract_employer": True,
    "contract_translated_yes": True,
    "insurance_from": "01/01/2024",
    "insurance_to": "31/12/2024",
    "insurance_company": "מגדל",
    "last_insurance_payment": "01/01/2025",

    "monthly_salary": "6000",
    "total_payment": "7500",
    "payment_date": "01",
    "payment_bank": True,

    "weekly_day_off": "שבת",
    "accommodation": "חדר פרטי עם שירותים",
    "notes": "העובדת מקצועית ומסורה",

    # Page 4 - Treatment plan
    "treatment_essence": "ביקור תקופתי לבדיקת תנאי העבודה",
    "treatment_employer_issues": True,
    "treatment_followup": True,

    "summary_employer": "המעסיק מרוצה מהשירות",
    "summary_caregiver": "המטפלת מתפקדת היטב",

    "attendee_employer": True,
    "attendee_worker": True,

    "signer_id": "987654321",
    "social_worker_name_signature": "שרה ישראלי",
    "responsible_worker_name": "רונית דגן",
    "responsible_worker_id": "111222333",
    "signature_date": "27/01/2025",
}

def main():
    template_path = "templates/template.pdf"
    output_path = "test_filled_comprehensive.pdf"

    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}")
        return

    print("Filling PDF with comprehensive test data...")
    fill_pdf_form(template_path, test_data, output_path)
    print(f"Created: {output_path}")

    # Open the file
    os.system(f"open {output_path}")

if __name__ == "__main__":
    main()
