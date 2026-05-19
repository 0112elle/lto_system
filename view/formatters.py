from typing import Tuple

def format_license(row: Tuple) -> str:
    # row: (License_number, License_type, License_status, License_issue_date, License_expiry_date, Dl_codes, Conditions)
    number = row[0] or '-'
    ltype = row[1] or '-'
    status = row[2] or '-'
    issue = row[3] or '-'
    expiry = row[4] or '-'
    dlcodes = row[5] or ''
    conds = row[6] or ''
    lines = [
        f"License No.:  {number} ({status} {ltype})",
        f"Issued:       {issue}",
        f"Expires:      {expiry}",
        f"DL codes:     {dlcodes}",
        f"Conditions:   {conds}",
    ]
    return "\n".join(lines)

def format_registration(row: Tuple) -> str:
    # row: (Registration_number, Registration_date, Expiration_date, Registration_status, Official_receipt_number, Official_receipt_date, Document_ref_no, Ownership_type, Transfer_reason, Ownership_start_date, Ownership_end_date, Vehicle_id)
    reg = row[0] or '-'
    reg_date = row[1] or '-'
    exp = row[2] or '-'
    status = row[3] or '-'
    ornum = row[4] or '-'
    ordate = row[5] or '-'
    owner_type = row[7] or '-'
    transfer = row[8] or '-'
    vid = row[11] or '-'
    return f"Registration {reg} | {status} | Expires: {exp} | OR: {ornum} ({ordate}) | Ownership: {owner_type} | Vehicle: {vid}"

def format_violation(row: Tuple) -> str:
    # row: (Violation_id, Violation_date, Fine_amount, Violation_status, Violation_Type, Plate_number, City, Region)
    vid = row[0]
    date = row[1]
    fine = row[2]
    status = row[3]
    vtype = row[4]
    plate = row[6] if len(row) > 6 else (row[5] if len(row)>5 else '-')
    loc = ''
    if len(row) > 6:
        city = row[6] or ''
        region = row[7] or ''
        loc = f"{city}, {region}".strip(', ')
    return f"Violation {vid}: {vtype} on {date} | Plate: {plate} | Fine: {fine} | Status: {status} | Location: {loc}"
