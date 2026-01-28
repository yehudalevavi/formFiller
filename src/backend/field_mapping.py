"""
Field mapping for the PDF form - CORRECTED based on detailed PDF analysis
Coordinates are in PDF points from bottom-left corner
PDF Size: 595.3 x 841.9 points (A4)

COORDINATE SYSTEM:
- x=0 is LEFT edge, x increases to the RIGHT
- y=0 is BOTTOM edge, y increases UPWARD
- For RTL Hebrew text: use align="right", x = RIGHT edge where text should END
- For LTR text (numbers, email): use align="left" (default), x = LEFT edge where text STARTS
"""

# PDF page dimensions (A4)
PAGE_WIDTH = 595.3
PAGE_HEIGHT = 841.9

# Font settings
HEBREW_FONT_SIZE = 9
CHECKBOX_SIZE = 10
HEBREW_FONT_NAME = "NotoSansHebrew"

# Field definitions with alignment support
# Based on actual PDF label positions:
# - Labels at y_top=N means label is at y_bottom = PAGE_HEIGHT - N - font_height
# - Input fields placed ~10-15 points below label bottom

FORM_FIELDS = {
    # ============================================================
    # PAGE 1 - Personal Details and Visit Info
    # ============================================================

    # Visit date fields - Labels at y_top=136, y_bottom≈698
    # Input should be at y≈693 (between labels at 698 and next row at 682)
    # Day label at x=56-64, Month at x=72-87, Year at x=102-114
    "visit_date_day": {"x": 58, "y": 693, "page": 0, "max_length": 2, "align": "left"},
    "visit_date_month": {"x": 76, "y": 693, "page": 0, "max_length": 2, "align": "left"},
    "visit_date_year": {"x": 100, "y": 693, "page": 0, "max_length": 4, "align": "left"},

    # ----- Employer Personal Details (פרטים אישיים של המעסיק) -----
    # Header at y_top=210, Labels at y_top=226 (y_bottom≈607)
    # Input at y≈593
    # שם משפחה at x=504-547 → right-align to x=547
    # שם פרטי at x=394-426 → right-align to x=426
    # מספר זהות at x=195-236 → numbers, left-align at x=195
    "employer_last_name": {"x": 547, "y": 593, "page": 0, "max_length": 20, "align": "right"},
    "employer_first_name": {"x": 426, "y": 593, "page": 0, "max_length": 20, "align": "right"},
    "employer_id": {"x": 145, "y": 593, "page": 0, "max_length": 9, "align": "left"},

    # ----- Employer Address (כתובת המעסיק) -----
    # Header at y_top=256, Labels at y_top=272 (y_bottom≈560)
    # Input at y≈546
    # רחוב at x=529-547 → right-align to x=547
    # מספר בית at x=389-425 → number, left-align at x=389
    # כניסה at x=355-376 → right-align to x=376
    # דירה at x=320-337 → number, left-align at x=320
    # ישוב at x=282-298 → right-align to x=298
    # מיקוד at x=111-131 → number, left-align at x=111
    "employer_street": {"x": 547, "y": 546, "page": 0, "max_length": 25, "align": "right"},
    "employer_house_number": {"x": 389, "y": 546, "page": 0, "max_length": 5, "align": "left"},
    "employer_entrance": {"x": 376, "y": 546, "page": 0, "max_length": 3, "align": "right"},
    "employer_apartment": {"x": 320, "y": 546, "page": 0, "max_length": 5, "align": "left"},
    "employer_city": {"x": 298, "y": 546, "page": 0, "max_length": 20, "align": "right"},
    "employer_zipcode": {"x": 55, "y": 546, "page": 0, "max_length": 7, "align": "left"},

    # ----- Employer Contact -----
    # Labels at y_top=307 (y_bottom≈525)
    # Input at y≈511
    # טלפון קווי at x=514-547 → numbers, but right-align for phone
    # טלפון נייד at x=392-426 → numbers
    # דואר אלקטרוני at x=246-298 → left-align email
    "employer_landline": {"x": 547, "y": 511, "page": 0, "max_length": 12, "align": "right"},
    "employer_mobile": {"x": 426, "y": 511, "page": 0, "max_length": 12, "align": "right"},
    "employer_email": {"x": 55, "y": 511, "page": 0, "max_length": 40, "align": "left"},

    # ----- Worker Details (פרטי העובד הזר) -----
    # Header at y_top=346 (y_bottom≈485)
    # מספר דרכון label at x=259-301
    # Input at y≈471
    "worker_passport": {"x": 200, "y": 471, "page": 0, "max_length": 15, "align": "left"},

    # Worker name fields - Labels at y_top=363 (y_bottom≈470)
    # Input at y≈456
    # שם משפחה at x=504-547 → right-align to x=547
    # שם פרטי at x=394-426 → right-align to x=426
    # ארץ מוצא at x=253-287 → right-align to x=287
    # טלפון נייד at x=120-154 → left-align number
    "worker_last_name": {"x": 547, "y": 456, "page": 0, "max_length": 20, "align": "right"},
    "worker_first_name": {"x": 426, "y": 456, "page": 0, "max_length": 20, "align": "right"},
    "worker_origin_country": {"x": 287, "y": 456, "page": 0, "max_length": 15, "align": "right"},
    "worker_mobile": {"x": 55, "y": 456, "page": 0, "max_length": 12, "align": "left"},

    # ----- Placement Info -----
    # Labels at y_top=393 (y_bottom≈440)
    # תאריך תחילת השמה at x=402-521
    # Input at y≈426
    "placement_start_date": {"x": 521, "y": 426, "page": 0, "max_length": 10, "align": "right"},

    # Importing agency - Israel/Abroad checkboxes
    # Template boxes at: x≈407.6, y≈434 (Israel) and x≈351.0, y≈435 (Abroad)
    "placement_israel": {"x": 408, "y": 424, "page": 0, "checkbox": True},
    "placement_abroad": {"x": 352, "y": 425, "page": 0, "checkbox": True},

    # Agency details - פרטי לשכה מאביינת at x=218-287
    "placement_agency": {"x": 287, "y": 426, "page": 0, "max_length": 30, "align": "right"},

    # ----- Worker Living Address (כתובת מגורים) -----
    # Labels at y_top=425 (y_bottom≈407)
    # Input at y≈393
    # רחוב at x=472-489 → right-align to x=489
    # מספר בית at x=342-378 → left-align at x=342
    # כניסה at x=310-331 → right-align to x=331
    # דירה at x=272-290 → left-align at x=272
    # ישוב at x=239-255 → right-align to x=255
    # יום חופשה at x=67-105 → right-align to x=105
    "worker_street": {"x": 489, "y": 393, "page": 0, "max_length": 25, "align": "right"},
    "worker_house_number": {"x": 342, "y": 393, "page": 0, "max_length": 5, "align": "left"},
    "worker_entrance": {"x": 331, "y": 393, "page": 0, "max_length": 3, "align": "right"},
    "worker_apartment": {"x": 272, "y": 393, "page": 0, "max_length": 5, "align": "left"},
    "worker_city": {"x": 255, "y": 393, "page": 0, "max_length": 20, "align": "right"},
    "worker_day_off": {"x": 105, "y": 393, "page": 0, "max_length": 15, "align": "right"},

    # ----- Previous Visit Dates (תאריכי ביקור אחרונים) -----
    # Header at y_top=462, Labels at y_top=483 (y_bottom≈350)
    # Input at y≈336
    # תאריך טרום השמה at x=469-539 → date, right-align
    # שם העו"ס at x=423-459 → right-align to x=459
    # תאריך אחרי השמה at x=247-318 → date, right-align
    # שם העו"ס at x=198-234 → right-align to x=234
    "pre_placement_date": {"x": 539, "y": 336, "page": 0, "max_length": 10, "align": "right"},
    "pre_placement_social_worker": {"x": 459, "y": 336, "page": 0, "max_length": 20, "align": "right"},
    "post_placement_date": {"x": 318, "y": 336, "page": 0, "max_length": 10, "align": "right"},
    "post_placement_social_worker": {"x": 234, "y": 336, "page": 0, "max_length": 20, "align": "right"},

    # ============================================================
    # PAGE 2 - Employer Assessment
    # ============================================================

    # תאור הופעה חיצונית - label at y_top=104 (y_bottom≈729)
    # Input at y≈715
    "appearance_description": {"x": 545, "y": 715, "page": 1, "max_length": 300, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # תאור מצב תזונתי - label at y_top=154 (y_bottom≈679)
    # Input at y≈665
    "nutritional_status": {"x": 545, "y": 665, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # תאור סימנים חיצוניים חריגים - label at y_top=202 (y_bottom≈630)
    # Input at y≈616
    "external_signs": {"x": 545, "y": 616, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # תאור מצב תיפקודי - label at y_top=249 (y_bottom≈583)
    # Input at y≈569
    "functional_status": {"x": 545, "y": 569, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # תאור מצבו הבריאותי - label at y_top=297 (y_bottom≈536)
    # Input at y≈522
    "health_status": {"x": 545, "y": 522, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # האם אושפז לאחרונה - Hospitalization checkboxes
    # Template boxes at: x≈527.8, y≈480 (Yes) and x≈499.7, y≈480 (No)
    "was_hospitalized_yes": {"x": 528, "y": 470, "page": 1, "checkbox": True},
    "was_hospitalized_no": {"x": 500, "y": 470, "page": 1, "checkbox": True},
    "hospitalization_where": {"x": 479, "y": 462, "page": 1, "max_length": 30, "align": "right"},
    "hospitalization_duration": {"x": 196, "y": 462, "page": 1, "max_length": 20, "align": "right"},

    # תאור קוגניטיבי - label at y_top=381 (y_bottom≈452)
    # Input at y≈438
    "cognitive_description": {"x": 545, "y": 438, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # התרשמות מתחזוקת הבית - label at y_top=430 (y_bottom≈402)
    # Input at y≈388
    "home_maintenance": {"x": 545, "y": 388, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # קניות מזון - label at y_top=479 (y_bottom≈354)
    # Input at y≈340
    "food_supply": {"x": 545, "y": 340, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # שביעות רצון הקשיש - label at y_top=527 (y_bottom≈306)
    # Input at y≈292
    "client_satisfaction": {"x": 545, "y": 292, "page": 1, "max_length": 100, "align": "right"},

    # שביעות רצון המשפחה - label at y_top=578 (y_bottom≈255)
    # Input at y≈241
    "family_satisfaction": {"x": 545, "y": 241, "page": 1, "max_length": 100, "align": "right"},

    # האם יש קשיים או תלונות - label at y_top=627 (y_bottom≈206)
    # Input at y≈192
    "service_difficulties": {"x": 545, "y": 192, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # בקשות מיוחדות של המעסיק - label at y_top=673 (y_bottom≈160)
    # Input at y≈146
    "special_requests": {"x": 545, "y": 146, "page": 1, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # ============================================================
    # PAGE 3 - Worker Report
    # ============================================================

    # תאור הופעה חיצונית (worker) - label at y_top=102 (y_bottom≈731)
    # Input at y≈717
    "worker_appearance": {"x": 545, "y": 717, "page": 2, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # האם העו"ז קיבל הדרכה - label at y_top=157 (y_bottom≈676)
    # Input at y≈662
    "worker_training": {"x": 545, "y": 662, "page": 2, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # מה הם תפקידי העו"ז - label at y_top=202 (estimated)
    # Input at y≈612
    "worker_duties": {"x": 545, "y": 612, "page": 2, "max_length": 300, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # האם העו"ז מרוצה - estimated
    # Input at y≈562
    "worker_satisfaction": {"x": 545, "y": 562, "page": 2, "max_length": 100, "align": "right"},

    # האם נצפו קשיים - estimated
    # Input at y≈512
    "work_difficulties": {"x": 545, "y": 512, "page": 2, "max_length": 200, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # האם יש הלימה - estimated
    # Input at y≈462
    "duties_match_satisfaction": {"x": 545, "y": 462, "page": 2, "max_length": 150, "align": "right"},

    # האם לעו"ז יש חברים - estimated
    # Input at y≈412
    "worker_has_friends": {"x": 545, "y": 412, "page": 2, "max_length": 100, "align": "right"},

    # תנאי העסקת העו"ז section - Contract checkboxes
    # Template boxes at y≈359: x=527.8 (employer), x=482.1 (worker), x=440.0 (other), x=341.8 (yes), x=314.5 (no)
    "contract_employer": {"x": 528, "y": 349, "page": 2, "checkbox": True},
    "contract_worker": {"x": 482, "y": 349, "page": 2, "checkbox": True},
    "contract_other": {"x": 440, "y": 349, "page": 2, "checkbox": True},

    # Contract translated checkboxes
    "contract_translated_yes": {"x": 342, "y": 349, "page": 2, "checkbox": True},
    "contract_translated_no": {"x": 315, "y": 349, "page": 2, "checkbox": True},

    # Insurance dates - מ at x=167, דע at x=100
    "insurance_from": {"x": 175, "y": 341, "page": 2, "max_length": 10, "align": "right"},
    "insurance_to": {"x": 109, "y": 341, "page": 2, "max_length": 10, "align": "right"},

    # Insurance company and payment
    "insurance_company": {"x": 545, "y": 318, "page": 2, "max_length": 30, "align": "right"},
    "last_insurance_payment": {"x": 375, "y": 318, "page": 2, "max_length": 15, "align": "right"},

    # Salary details
    "monthly_salary": {"x": 545, "y": 289, "page": 2, "max_length": 10, "align": "right"},
    "total_payment": {"x": 420, "y": 289, "page": 2, "max_length": 10, "align": "right"},
    "payment_date": {"x": 340, "y": 289, "page": 2, "max_length": 10, "align": "right"},

    # Payment method checkboxes
    # Template boxes at y≈293: x=295.5 (check), x=262.5 (bank), x=189.5 (cash), x=151.7 (other)
    "payment_check": {"x": 296, "y": 283, "page": 2, "checkbox": True},
    "payment_bank": {"x": 263, "y": 283, "page": 2, "checkbox": True},
    "payment_cash": {"x": 190, "y": 283, "page": 2, "checkbox": True},
    "payment_other": {"x": 152, "y": 283, "page": 2, "checkbox": True},

    # יום החופש השבועי and accommodation
    "weekly_day_off": {"x": 547, "y": 254, "page": 2, "max_length": 15, "align": "right"},
    "accommodation": {"x": 461, "y": 254, "page": 2, "max_length": 200, "align": "right"},

    # הערות
    "notes": {"x": 545, "y": 180, "page": 2, "max_length": 300, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # ============================================================
    # PAGE 4 - Treatment Plan
    # ============================================================

    # מהות הטיפול - label at y_top≈88 (y_bottom≈728)
    # Input at y≈700
    "treatment_essence": {"x": 545, "y": 700, "page": 3, "max_length": 400, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # Treatment type checkboxes
    # Template boxes at y≈722-723: x=531.3, x=422.5, x=305.3, x=268.8, x=230.9, x=135.5
    "treatment_employer_issues": {"x": 531, "y": 713, "page": 3, "checkbox": True},
    "treatment_worker_issues": {"x": 423, "y": 713, "page": 3, "checkbox": True},
    "treatment_mediation": {"x": 305, "y": 713, "page": 3, "checkbox": True},
    "treatment_followup": {"x": 269, "y": 713, "page": 3, "checkbox": True},
    "treatment_referral": {"x": 231, "y": 713, "page": 3, "checkbox": True},
    "treatment_family_report": {"x": 136, "y": 713, "page": 3, "checkbox": True},

    # סיכום והתרשמות - בנוגע למעסיק at y≈634
    "summary_employer": {"x": 545, "y": 620, "page": 3, "max_length": 300, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # בנוגע למטפל at y≈590
    "summary_caregiver": {"x": 545, "y": 575, "page": 3, "max_length": 300, "multiline": True, "width": 490, "line_height": 12, "align": "right"},

    # נוכחים בביקור - Attendee checkboxes
    # Template boxes at y≈546-547: x=477.3 (employer), x=430.2 (family), x=369.2 (worker), x=316.5 (office rep), x=222.5 (other)
    "attendee_employer": {"x": 477, "y": 537, "page": 3, "checkbox": True},
    "attendee_family": {"x": 430, "y": 537, "page": 3, "checkbox": True},
    "attendee_worker": {"x": 369, "y": 537, "page": 3, "checkbox": True},
    "attendee_office_rep": {"x": 317, "y": 537, "page": 3, "checkbox": True},
    "attendee_other": {"x": 223, "y": 537, "page": 3, "checkbox": True},

    # Signature section - תוהז.ת at x=197-223 (y≈511)
    "signer_id": {"x": 197, "y": 503, "page": 3, "max_length": 12, "align": "left"},

    # שם העובד הסוציאלי/בעל תפקיד at y≈444
    "social_worker_name_signature": {"x": 545, "y": 436, "page": 3, "max_length": 30, "align": "right"},

    # שם העובד הסוציאלי האחראי at y≈421
    "responsible_worker_name": {"x": 545, "y": 413, "page": 3, "max_length": 30, "align": "right"},
    "responsible_worker_id": {"x": 197, "y": 413, "page": 3, "max_length": 12, "align": "left"},

    # תאריך הביקור at y≈356
    "signature_date": {"x": 526, "y": 348, "page": 3, "max_length": 12, "align": "right"},
}
