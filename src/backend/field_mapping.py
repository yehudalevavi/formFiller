"""
Field mapping for the PDF form
Coordinates are in PDF points (72 points = 1 inch) from bottom-left corner
"""

# PDF page dimensions (A4 in points: 595.27 x 841.89)
PAGE_WIDTH = 595.27
PAGE_HEIGHT = 841.89

# Field definitions with coordinates (x, y, page_number)
# For RTL Hebrew text, we'll need to position from right side
FORM_FIELDS = {
    # Page 1 - Header and Personal Details
    "visit_date_day": {"x": 520, "y": 750, "page": 0, "max_length": 2},
    "visit_date_month": {"x": 490, "y": 750, "page": 0, "max_length": 2},
    "visit_date_year": {"x": 450, "y": 750, "page": 0, "max_length": 4},
    "office_name": {"x": 400, "y": 750, "page": 0, "max_length": 50},

    # Employer address
    "employer_street": {"x": 500, "y": 720, "page": 0, "max_length": 30},
    "employer_house_number": {"x": 420, "y": 720, "page": 0, "max_length": 5},
    "employer_entrance": {"x": 380, "y": 720, "page": 0, "max_length": 3},
    "employer_apartment": {"x": 340, "y": 720, "page": 0, "max_length": 5},
    "employer_city": {"x": 280, "y": 720, "page": 0, "max_length": 20},
    "employer_phone": {"x": 180, "y": 720, "page": 0, "max_length": 15},

    # Social worker details
    "social_worker_name": {"x": 450, "y": 690, "page": 0, "max_length": 40},
    "social_worker_phone": {"x": 280, "y": 690, "page": 0, "max_length": 15},

    # Employer personal details
    "employer_last_name": {"x": 500, "y": 650, "page": 0, "max_length": 25},
    "employer_first_name": {"x": 400, "y": 650, "page": 0, "max_length": 25},
    "employer_id": {"x": 280, "y": 650, "page": 0, "max_length": 12},

    # Employer current address
    "employer_current_street": {"x": 500, "y": 620, "page": 0, "max_length": 30},
    "employer_current_house": {"x": 420, "y": 620, "page": 0, "max_length": 5},
    "employer_current_entrance": {"x": 380, "y": 620, "page": 0, "max_length": 3},
    "employer_current_apartment": {"x": 340, "y": 620, "page": 0, "max_length": 5},
    "employer_current_city": {"x": 250, "y": 620, "page": 0, "max_length": 20},
    "employer_current_zipcode": {"x": 180, "y": 620, "page": 0, "max_length": 7},

    # Employer contact
    "employer_landline": {"x": 450, "y": 590, "page": 0, "max_length": 15},
    "employer_mobile": {"x": 320, "y": 590, "page": 0, "max_length": 15},
    "employer_email": {"x": 150, "y": 590, "page": 0, "max_length": 40},

    # Foreign worker details
    "worker_passport": {"x": 500, "y": 560, "page": 0, "max_length": 15},
    "worker_last_name": {"x": 400, "y": 530, "page": 0, "max_length": 25},
    "worker_first_name": {"x": 280, "y": 530, "page": 0, "max_length": 25},
    "worker_country": {"x": 180, "y": 530, "page": 0, "max_length": 20},
    "worker_mobile": {"x": 80, "y": 530, "page": 0, "max_length": 15},

    # Immigration details
    "entry_date": {"x": 450, "y": 500, "page": 0, "max_length": 10},
    "from_abroad": {"x": 350, "y": 500, "page": 0, "checkbox": True},
    "from_israel": {"x": 300, "y": 500, "page": 0, "checkbox": True},
    "from_other_employer": {"x": 220, "y": 500, "page": 0, "checkbox": True},

    # Page 2 - Assessment sections
    "appearance_description": {"x": 100, "y": 700, "page": 1, "max_length": 200, "multiline": True},
    "nutritional_status": {"x": 100, "y": 650, "page": 1, "max_length": 200, "multiline": True},
    "external_signs": {"x": 100, "y": 600, "page": 1, "max_length": 200, "multiline": True},
    "functional_status": {"x": 100, "y": 550, "page": 1, "max_length": 200, "multiline": True},
    "health_status": {"x": 100, "y": 500, "page": 1, "max_length": 200, "multiline": True},

    # Hospitalization
    "was_hospitalized": {"x": 400, "y": 450, "page": 1, "checkbox": True},
    "hospitalization_where": {"x": 300, "y": 450, "page": 1, "max_length": 30},
    "hospitalization_duration": {"x": 150, "y": 450, "page": 1, "max_length": 20},

    # Cognitive and other assessments
    "cognitive_description": {"x": 100, "y": 400, "page": 1, "max_length": 200, "multiline": True},
    "home_maintenance": {"x": 100, "y": 350, "page": 1, "max_length": 200, "multiline": True},
    "food_supply": {"x": 100, "y": 300, "page": 1, "max_length": 200, "multiline": True},
    "client_satisfaction": {"x": 100, "y": 250, "page": 1, "max_length": 100},
    "family_satisfaction": {"x": 100, "y": 220, "page": 1, "max_length": 100},
    "service_difficulties": {"x": 100, "y": 190, "page": 1, "max_length": 200, "multiline": True},
    "special_requests": {"x": 100, "y": 140, "page": 1, "max_length": 200, "multiline": True},

    # Page 3 - Worker report
    "worker_appearance": {"x": 100, "y": 700, "page": 2, "max_length": 200, "multiline": True},
    "worker_received_training": {"x": 400, "y": 650, "page": 2, "checkbox": True},
    "worker_duties": {"x": 100, "y": 600, "page": 2, "max_length": 300, "multiline": True},
    "worker_satisfaction": {"x": 350, "y": 520, "page": 2, "max_length": 50},
    "work_difficulties": {"x": 350, "y": 490, "page": 2, "max_length": 50},
    "duties_match_needs": {"x": 350, "y": 460, "page": 2, "max_length": 50},
    "worker_has_friends": {"x": 350, "y": 430, "page": 2, "checkbox": True},

    # Employment conditions
    "medical_insurance_valid": {"x": 450, "y": 380, "page": 2, "checkbox": True},
    "insurance_from": {"x": 400, "y": 380, "page": 2, "max_length": 10},
    "insurance_to": {"x": 350, "y": 380, "page": 2, "max_length": 10},
    "contract_with_employer": {"x": 280, "y": 380, "page": 2, "checkbox": True},
    "contract_with_other": {"x": 230, "y": 380, "page": 2, "checkbox": True},

    # Payment details
    "insurance_company": {"x": 450, "y": 340, "page": 2, "max_length": 30},
    "last_payment_date": {"x": 320, "y": 340, "page": 2, "max_length": 10},
    "monthly_salary": {"x": 450, "y": 310, "page": 2, "max_length": 10},
    "payment_date": {"x": 350, "y": 310, "page": 2, "max_length": 10},
    "total_payment": {"x": 250, "y": 310, "page": 2, "max_length": 10},
    "payment_method_cash": {"x": 180, "y": 310, "page": 2, "checkbox": True},
    "payment_method_bank": {"x": 130, "y": 310, "page": 2, "checkbox": True},
    "payment_method_other": {"x": 80, "y": 310, "page": 2, "checkbox": True},

    # Accommodation
    "accommodation_description": {"x": 100, "y": 260, "page": 2, "max_length": 200, "multiline": True},
    "weekly_day_off": {"x": 100, "y": 220, "page": 2, "max_length": 20},

    "additional_notes": {"x": 100, "y": 180, "page": 2, "max_length": 300, "multiline": True},

    # Page 4 - Treatment plan and signatures
    "treatment_plan_description": {"x": 100, "y": 650, "page": 3, "max_length": 400, "multiline": True},
    "treatment_types.elderly_issues": {"x": 450, "y": 550, "page": 3, "checkbox": True},
    "treatment_types.caregiver_issues": {"x": 380, "y": 550, "page": 3, "checkbox": True},
    "treatment_types.liaison": {"x": 320, "y": 550, "page": 3, "checkbox": True},
    "treatment_types.follow_up": {"x": 260, "y": 550, "page": 3, "checkbox": True},
    "treatment_types.referral": {"x": 200, "y": 550, "page": 3, "checkbox": True},
    "treatment_types.family_report": {"x": 140, "y": 550, "page": 3, "checkbox": True},

    "summary_employer": {"x": 100, "y": 480, "page": 3, "max_length": 300, "multiline": True},
    "summary_caregiver": {"x": 100, "y": 400, "page": 3, "max_length": 300, "multiline": True},

    # Attendees
    "attendees_employer": {"x": 480, "y": 330, "page": 3, "checkbox": True},
    "attendees_family": {"x": 420, "y": 330, "page": 3, "checkbox": True},
    "attendees_worker": {"x": 360, "y": 330, "page": 3, "checkbox": True},
    "attendees_office_rep": {"x": 280, "y": 330, "page": 3, "checkbox": True},
    "attendees_other": {"x": 220, "y": 330, "page": 3, "checkbox": True},

    # Signatures
    "social_worker_id": {"x": 450, "y": 280, "page": 3, "max_length": 12},
    "social_worker_signature_name": {"x": 280, "y": 280, "page": 3, "max_length": 40},
    "social_worker_signature_date": {"x": 120, "y": 280, "page": 3, "max_length": 10},

    "responsible_worker_id": {"x": 450, "y": 240, "page": 3, "max_length": 12},
    "responsible_worker_name": {"x": 280, "y": 240, "page": 3, "max_length": 40},

    "supervisor_confirmation_date": {"x": 450, "y": 180, "page": 3, "max_length": 10},
}

# Font settings for Hebrew text
HEBREW_FONT_NAME = "Helvetica"
HEBREW_FONT_SIZE = 10
CHECKBOX_SIZE = 8
