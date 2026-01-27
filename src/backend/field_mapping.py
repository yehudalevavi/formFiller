"""
Field mapping for the PDF form - UPDATED based on actual PDF analysis
Coordinates are in PDF points from bottom-left corner
PDF Size: 612 x 792 points (US Letter)

NOTE: Many fields on Page 1 are PRE-FILLED in the template.
Only mapping fields that need user input.
"""

# PDF page dimensions
PAGE_WIDTH = 612
PAGE_HEIGHT = 792

# Font settings
HEBREW_FONT_SIZE = 9
CHECKBOX_SIZE = 10

# Field definitions - ONLY fields that need to be filled
# Coordinates based on actual PDF analysis
FORM_FIELDS = {
    # ============================================================
    # PAGE 1 - Visit Date (most other fields are pre-filled)
    # ============================================================
    # Date fields at y=715 area, to the left of "תאריך הביקור"
    "visit_date_day": {"x": 95, "y": 700, "page": 0, "max_length": 2},
    "visit_date_month": {"x": 135, "y": 700, "page": 0, "max_length": 2},
    "visit_date_year": {"x": 165, "y": 700, "page": 0, "max_length": 4},

    # "תאריכי ביקור אחרונים" section - if needed
    # Located at y=351.7 area

    # ============================================================
    # PAGE 2 - Employer Assessment (all text areas need filling)
    # ============================================================

    # תאור הופעה חיצונית - below label at y=734.9, input area below
    "appearance_description": {"x": 50, "y": 710, "page": 1, "max_length": 300, "multiline": True, "width": 520, "line_height": 12},

    # תאור מצב תזונתי - label at y=681.6
    "nutritional_status": {"x": 50, "y": 658, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # תאור סמממנים חיצוניים חריגים - label at y=629.9
    "external_signs": {"x": 50, "y": 606, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # תאור מצב תיפקודי - label at y=579.6
    "functional_status": {"x": 50, "y": 556, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # תאור מצבו הבריאותי - label at y=528.6
    "health_status": {"x": 50, "y": 505, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # האם אושפז לאחרונה - checkboxes at y=458.1
    "was_hospitalized_yes": {"x": 538, "y": 458, "page": 1, "checkbox": True},
    "was_hospitalized_no": {"x": 500, "y": 458, "page": 1, "checkbox": True},
    "hospitalization_where": {"x": 350, "y": 458, "page": 1, "max_length": 30},
    "hospitalization_duration": {"x": 150, "y": 458, "page": 1, "max_length": 20},

    # תאור קוגניטיבי - label at y=438.6
    "cognitive_description": {"x": 50, "y": 415, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # התרשמות מתחזוקת הבית - label at y=386.1
    "home_maintenance": {"x": 50, "y": 363, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # קניות מזון - label at y=334.4
    "food_supply": {"x": 50, "y": 311, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # שביעות רצון הקשיש - label at y=282.6
    "client_satisfaction": {"x": 50, "y": 260, "page": 1, "max_length": 100},

    # שביעות רצון המשפחה - label at y=228.6
    "family_satisfaction": {"x": 50, "y": 206, "page": 1, "max_length": 100},

    # האם יש קשיים או תלונות - label at y=176.1
    "service_difficulties": {"x": 50, "y": 153, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # בקשות מיוחדות של המעסיק - label at y=126.6
    "special_requests": {"x": 50, "y": 103, "page": 1, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # ============================================================
    # PAGE 3 - Worker Report
    # ============================================================

    # תאור הופעה חיצונית (worker) - label at y=737.1
    "worker_appearance": {"x": 50, "y": 714, "page": 2, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # האם העו"ז קיבל הדרכה - label at y=678.6
    "worker_training": {"x": 50, "y": 655, "page": 2, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # מה הם תפקידי העו"ז - label at y=629.9
    "worker_duties": {"x": 50, "y": 606, "page": 2, "max_length": 300, "multiline": True, "width": 520, "line_height": 12},

    # האם העו"ז מרוצה - label at y=579.6
    "worker_satisfaction": {"x": 50, "y": 556, "page": 2, "max_length": 100},

    # האם נצפו קשיים - label at y=528.6
    "work_difficulties": {"x": 50, "y": 505, "page": 2, "max_length": 200, "multiline": True, "width": 520, "line_height": 12},

    # האם יש הלימה - label at y=476.9
    "duties_match_satisfaction": {"x": 50, "y": 454, "page": 2, "max_length": 150},

    # האם לעו"ז יש חברים - label at y=425.1
    "worker_has_friends": {"x": 50, "y": 402, "page": 2, "max_length": 100},

    # תנאי העסקת העו"ז section - y=344.9 to y=258.6
    # Contract checkboxes
    "contract_employer": {"x": 540, "y": 330, "page": 2, "checkbox": True},
    "contract_worker": {"x": 500, "y": 330, "page": 2, "checkbox": True},
    "contract_other": {"x": 460, "y": 330, "page": 2, "checkbox": True},

    # Contract translated checkbox
    "contract_translated_yes": {"x": 400, "y": 330, "page": 2, "checkbox": True},
    "contract_translated_no": {"x": 360, "y": 330, "page": 2, "checkbox": True},

    # Insurance dates
    "insurance_from": {"x": 250, "y": 330, "page": 2, "max_length": 10},
    "insurance_to": {"x": 180, "y": 330, "page": 2, "max_length": 10},

    # Insurance company and payment - y=310.4
    "insurance_company": {"x": 450, "y": 288, "page": 2, "max_length": 30},
    "last_insurance_payment": {"x": 250, "y": 288, "page": 2, "max_length": 15},

    # Salary details - y=274.4
    "monthly_salary": {"x": 520, "y": 252, "page": 2, "max_length": 10},
    "total_payment": {"x": 420, "y": 252, "page": 2, "max_length": 10},
    "payment_date": {"x": 320, "y": 252, "page": 2, "max_length": 10},

    # Payment method checkboxes - y=258.6
    "payment_check": {"x": 460, "y": 258, "page": 2, "checkbox": True},
    "payment_bank": {"x": 400, "y": 258, "page": 2, "checkbox": True},
    "payment_cash": {"x": 350, "y": 258, "page": 2, "checkbox": True},
    "payment_other": {"x": 310, "y": 258, "page": 2, "checkbox": True},

    # יום החופש השבועי and accommodation - y=240.6
    "weekly_day_off": {"x": 520, "y": 218, "page": 2, "max_length": 15},
    "accommodation": {"x": 50, "y": 218, "page": 2, "max_length": 200},

    # הערות - y=165.0
    "notes": {"x": 50, "y": 142, "page": 2, "max_length": 300, "multiline": True, "width": 520, "line_height": 12},

    # ============================================================
    # PAGE 4 - Treatment Plan
    # ============================================================

    # מהות הטיפול - label at y=736.4, input below
    "treatment_essence": {"x": 50, "y": 693, "page": 3, "max_length": 400, "multiline": True, "width": 520, "line_height": 12},

    # Treatment type checkboxes - y=717.6
    "treatment_employer_issues": {"x": 500, "y": 717, "page": 3, "checkbox": True},
    "treatment_worker_issues": {"x": 410, "y": 717, "page": 3, "checkbox": True},
    "treatment_mediation": {"x": 340, "y": 717, "page": 3, "checkbox": True},
    "treatment_followup": {"x": 290, "y": 717, "page": 3, "checkbox": True},
    "treatment_referral": {"x": 220, "y": 717, "page": 3, "checkbox": True},
    "treatment_family_report": {"x": 130, "y": 717, "page": 3, "checkbox": True},

    # סיכום והתרשמות - label at y=652.4
    # בנוגע למעסיק - y=634.4
    "summary_employer": {"x": 50, "y": 611, "page": 3, "max_length": 300, "multiline": True, "width": 520, "line_height": 12},

    # בנוגע למטפל - y=586.4
    "summary_caregiver": {"x": 50, "y": 563, "page": 3, "max_length": 300, "multiline": True, "width": 520, "line_height": 12},

    # נוכחים בביקור checkboxes - y=530.1
    "attendee_employer": {"x": 480, "y": 530, "page": 3, "checkbox": True},
    "attendee_family": {"x": 410, "y": 530, "page": 3, "checkbox": True},
    "attendee_worker": {"x": 340, "y": 530, "page": 3, "checkbox": True},
    "attendee_office_rep": {"x": 250, "y": 530, "page": 3, "checkbox": True},
    "attendee_other": {"x": 160, "y": 530, "page": 3, "checkbox": True},

    # Signature section - y=502.4
    "signer_id": {"x": 100, "y": 502, "page": 3, "max_length": 12},

    # שם העובד הסוציאלי/בעל תפקיד - y=430.4
    "social_worker_name_signature": {"x": 300, "y": 430, "page": 3, "max_length": 30},

    # שם העובד הסוציאלי האחראי - y=406.4
    "responsible_worker_name": {"x": 300, "y": 406, "page": 3, "max_length": 30},
    "responsible_worker_id": {"x": 100, "y": 406, "page": 3, "max_length": 12},

    # תאריך הביקור (signature section) - y=336.6
    "signature_date": {"x": 450, "y": 336, "page": 3, "max_length": 12},
}
