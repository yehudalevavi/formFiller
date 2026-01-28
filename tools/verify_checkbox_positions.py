#!/usr/bin/env python3
"""
Script to verify checkbox positions by comparing template boxes vs. our X positions
"""
import pdfplumber

def verify_checkboxes(template_path, output_path):
    """Compare checkbox box positions with X mark positions"""

    # Expected checkbox positions from field_mapping.py (after fix)
    checkbox_fields = {
        0: {  # Page 1
            "placement_israel": {"x": 408, "y": 433},
            "placement_abroad": {"x": 352, "y": 433},
        },
        1: {  # Page 2
            "was_hospitalized_yes": {"x": 528, "y": 478},
            "was_hospitalized_no": {"x": 500, "y": 478},
        },
        2: {  # Page 3
            "contract_employer": {"x": 528, "y": 357},
            "contract_worker": {"x": 482, "y": 357},
            "contract_other": {"x": 440, "y": 357},
            "contract_translated_yes": {"x": 342, "y": 357},
            "contract_translated_no": {"x": 315, "y": 357},
            "payment_check": {"x": 296, "y": 291},
            "payment_bank": {"x": 263, "y": 291},
            "payment_cash": {"x": 190, "y": 291},
            "payment_other": {"x": 152, "y": 291},
        },
        3: {  # Page 4
            "treatment_employer_issues": {"x": 531, "y": 721},
            "treatment_worker_issues": {"x": 423, "y": 721},
            "treatment_mediation": {"x": 305, "y": 721},
            "treatment_followup": {"x": 269, "y": 721},
            "treatment_referral": {"x": 231, "y": 721},
            "treatment_family_report": {"x": 136, "y": 721},
            "attendee_employer": {"x": 477, "y": 545},
            "attendee_family": {"x": 430, "y": 545},
            "attendee_worker": {"x": 369, "y": 545},
            "attendee_office_rep": {"x": 317, "y": 545},
            "attendee_other": {"x": 223, "y": 545},
        },
    }

    print("CHECKBOX POSITION VERIFICATION")
    print("=" * 80)

    with pdfplumber.open(template_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            if page_num not in checkbox_fields:
                continue

            print(f"\n--- Page {page_num + 1} ---")
            print(f"Page height: {page.height}")

            # Find small rectangles (checkbox boxes)
            rects = page.rects
            small_rects = [r for r in rects if
                          8 <= r['width'] <= 15 and
                          8 <= r['height'] <= 15]

            # Convert to PDF coordinates and sort
            boxes = []
            for rect in small_rects:
                pdf_y = page.height - rect['top']
                boxes.append({
                    "x": rect['x0'],
                    "y": pdf_y,
                    "width": rect['width'],
                    "height": rect['height']
                })

            # Group boxes by approximate Y position
            y_groups = {}
            for box in boxes:
                y_key = round(box['y'] / 20) * 20
                if y_key not in y_groups:
                    y_groups[y_key] = []
                y_groups[y_key].append(box)

            # Verify each checkbox field
            for field_name, expected_pos in checkbox_fields[page_num].items():
                # Find closest box
                closest_box = None
                min_dist = float('inf')
                for box in boxes:
                    dist = ((box['x'] - expected_pos['x'])**2 + (box['y'] - expected_pos['y'])**2)**0.5
                    if dist < min_dist:
                        min_dist = dist
                        closest_box = box

                if closest_box:
                    dx = expected_pos['x'] - closest_box['x']
                    dy = expected_pos['y'] - closest_box['y']
                    status = "OK" if min_dist < 5 else "ADJUST"
                    print(f"{field_name}:")
                    print(f"  Expected: x={expected_pos['x']}, y={expected_pos['y']}")
                    print(f"  Box at:   x={closest_box['x']:.1f}, y={closest_box['y']:.1f}")
                    print(f"  Offset:   dx={dx:.1f}, dy={dy:.1f}, dist={min_dist:.1f} [{status}]")


if __name__ == "__main__":
    verify_checkboxes("templates/template.pdf", "test_output.pdf")
