#!/usr/bin/env python3
"""
Test script to verify PDF coordinate mapping
Creates a test PDF with sample data to verify field positions
"""
import sys
sys.path.insert(0, 'src')

from backend.pdf_filler import fill_pdf_form

# Test data in Hebrew
test_data = {
    # Page 1 - Header
    "visit_date_day": "15",
    "visit_date_month": "01",
    "visit_date_year": "2025",
    "office_name": "משרד רווחה תל אביב",

    # Employer address
    "employer_street": "בן יהודה",
    "employer_house_number": "32",
    "employer_entrance": "א",
    "employer_apartment": "5",
    "employer_city": "תל-אביב",
    "employer_phone": "03-6291646",

    # Social worker
    "social_worker_name": "דליה ארנסון",
    "social_worker_phone": "052-1234567",

    # Employer details
    "employer_last_name": "אברמוב",
    "employer_first_name": "רוזה",
    "employer_id": "014432488",

    # Current address
    "employer_current_street": "מרבד הקסמים",
    "employer_current_house": "2",
    "employer_current_city": "חולון",
    "employer_current_zipcode": "58100",
    "employer_landline": "03-5551234",
    "employer_mobile": "052-4878625",
    "employer_email": "test@example.com",

    # Worker details
    "worker_passport": "FA0664465",
    "worker_last_name": "Rakhimova",
    "worker_first_name": "Shakhnoza",
    "worker_country": "אוזבקיסטן",
    "worker_mobile": "055-2386040",
    "entry_date": "06/12/2022",
    "from_abroad": True,

    # Page 2 - Assessments
    "appearance_description": "מטופח, לבוש בהתאם לעונה, רגוע",
    "nutritional_status": "נראה בהתאם לגילו, משקל תקין",
    "external_signs": "אין סימנים חריגים",
    "functional_status": "עצמאי במעברים, זקוק לעזרה בהתלבשות",
    "health_status": "מחלות כרוניות: לחץ דם גבוה, סוכרת",
    "was_hospitalized": False,
    "cognitive_description": "תקין להבנה והבעה, זיכרון תקין",
    "home_maintenance": "הבית מאוחזק היטב, נקי ומסודר",
    "food_supply": "המשפחה קונה עבור הקשיש ועובד הזר",
    "client_satisfaction": "גבוהה",
    "family_satisfaction": "גבוהה",
    "service_difficulties": "אין",
    "special_requests": "אין בקשות מיוחדות",

    # Page 3 - Worker report
    "worker_appearance": "מטופחת, לבושה בהתאם לעונה",
    "worker_received_training": True,
    "worker_duties": "ניקיון, כביסה, רחצה, החתלה, הלבשה, מתן תרופות, ליווי לטיפולים",
    "worker_satisfaction": "מרוצה",
    "work_difficulties": "לא נצפו",
    "duties_match_needs": "כן",
    "worker_has_friends": True,
    "medical_insurance_valid": True,
    "insurance_from": "01/01/2025",
    "insurance_to": "31/12/2025",
    "contract_with_employer": True,
    "insurance_company": "הראל",
    "last_payment_date": "01/01/2025",
    "monthly_salary": "5300",
    "payment_date": "1",
    "total_payment": "5300",
    "payment_method_bank": True,
    "accommodation_description": "חדר שינה נפרד, מיטה, ארון בגדים, חימום, טלוויזיה",
    "weekly_day_off": "שבת",
    "additional_notes": "הביקור עבר בהצלחה, אין בעיות מיוחדות",

    # Page 4 - Treatment plan
    "treatment_plan_description": "המשך מעקב רגיל, בדיקת תנאי העסקה, טיפול בבעיות של הקשיש",
    "treatment_types": {
        "elderly_issues": True,
        "follow_up": True,
    },
    "summary_employer": "הקשיש במצב טוב, מקבל טיפול הולם",
    "summary_caregiver": "העובדת הזרה מטפלת היטב, מתאימה לתפקיד",
    "attendees_employer": True,
    "attendees_family": True,
    "attendees_worker": True,
    "social_worker_id": "123456789",
    "social_worker_signature_name": "דליה ארנסון",
    "social_worker_signature_date": "15/01/2025",
    "responsible_worker_name": "משה כהן",
    "responsible_worker_id": "987654321",
    "supervisor_confirmation_date": "15/01/2025",
}

if __name__ == "__main__":
    template_path = "templates/template.pdf"
    output_path = "test_output.pdf"

    print("Filling PDF form with test data...")
    try:
        fill_pdf_form(template_path, test_data, output_path)
        print(f"Success! Test PDF created at: {output_path}")
        print("Please open the file and verify field positions.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
