from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Claim, TravelPlan, ClaimStatus
from datetime import datetime

def validate_claim(db: Session, claim_data: dict, employee_id: int):
    """
    Validates a claim against company policies.
    Returns: (is_valid: bool, message: str)
    """
    amount = float(claim_data.get("amount", 0))
    category = claim_data.get("category", "Others")
    date_str = claim_data.get("date")
    gst = claim_data.get("gst")
    
    if not date_str:
        return False, "Date is missing from receipt."
    
    # Attempt to parse date in multiple formats, including '12-Feb-2025'
    claim_date = None
    parse_formats = [
        "%Y-%m-%d",    # 2025-02-12
        "%d-%m-%Y",    # 12-02-2025
        "%d-%b-%Y",    # 12-Feb-2025
        "%d/%m/%Y",    # 12/02/2025
        "%d/%b/%Y",    # 12/Feb/2025
        "%d %b %Y",    # 12 Feb 2025
        "%b %d, %Y",   # Feb 12, 2025
    ]
    for fmt in parse_formats:
        try:
            claim_date = datetime.strptime(date_str, fmt).date()
            break
        except ValueError:
            continue
    if not claim_date:
        return False, f"Invalid date format: {date_str}"

    # 1. Duplicate Check
    # Check if a claim with same amount, date, and employee already exists (and isn't rejected)
    existing_claim = db.query(Claim).filter(
    Claim.employee_id == employee_id,
    Claim.amount == amount,
    Claim.date == claim_date,
    Claim.status != ClaimStatus.REJECTED.value
    ).first()
    
    if existing_claim:
        return False, "Duplicate claim detected (same amount and date)."

    # 2. Food Limit Check
    if category == "Food":
        # Check total food claims for this day
        daily_food_total = 0
        same_day_food_claims = db.query(Claim).filter(
            Claim.employee_id == employee_id,
            Claim.date == claim_date,
            Claim.category == "Food",
            Claim.status != ClaimStatus.REJECTED.value
        ).all()
        
        for c in same_day_food_claims:
            daily_food_total += c.amount
        
        if daily_food_total + amount > 500:
            return False, f"Daily food limit exceeded. Used: {daily_food_total}, Requested: {amount}, Limit: 500."

    # 3. Hotel GST Check
    if category == "Hotel" and amount > 1000 and not gst:
        return False, "GST number is mandatory for Hotel claims above ₹1000."

    # 4. Travel Plan Check
    if category == "Travel":
        # Find an approved travel plan that covers this date
        travel_plan = db.query(TravelPlan).filter(
            TravelPlan.employee_id == employee_id,
            TravelPlan.start_date <= claim_date,
            TravelPlan.end_date >= claim_date,
            TravelPlan.status == "approved"
        ).first()
        
        if not travel_plan:
            return False, "No approved travel plan found for this date."
        
        # Optional: Check if travel plan budget is exceeded (can be done in Budget module too)

    return True, "Claim is valid."
