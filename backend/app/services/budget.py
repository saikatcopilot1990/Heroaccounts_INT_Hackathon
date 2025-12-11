from sqlalchemy.orm import Session
from app.models import Budget, TravelPlan, Claim, ClaimStatus

def check_budget(db: Session, claim_data: dict, employee_id: int):
    """
    Checks if there is sufficient budget for the claim.
    Returns: (is_eligible: bool, message: str, remaining_budget: float)
    """
    amount = float(claim_data.get("amount", 0))
    category = claim_data.get("category", "Others")
    date_str = claim_data.get("date")
    
    # Logic:
    # 1. If Category is Travel, check TravelPlan budget
    # 2. Else, check Project Budget (if project code is provided, or default to a general budget)
    
    # For this implementation, we'll simplify:
    # - Travel claims -> TravelPlan
    # - Other claims -> Project Budget (if we had a project code in claim, but we don't in extraction yet)
    # Let's assume non-travel claims link to a generic Department Budget or Project Budget if we can infer it.
    
    if category == "Travel":
        # Find active travel plan
        # (In a real app, we'd pass the travel_plan_id if selected by user, or infer from date)
        # Here we infer from date again, similar to policy check
        from datetime import datetime
        try:
             claim_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
             return False, "Invalid date", 0.0

        travel_plan = db.query(TravelPlan).filter(
            TravelPlan.employee_id == employee_id,
            TravelPlan.start_date <= claim_date,
            TravelPlan.end_date >= claim_date,
            TravelPlan.status == "approved"
        ).first()
        
        if not travel_plan:
            return False, "No active travel plan for this date.", 0.0
            
        # Calculate used budget in this plan
        used_amount = 0
        plan_claims = db.query(Claim).filter(
            Claim.travel_plan_id == travel_plan.id,
            Claim.status != ClaimStatus.REJECTED
        ).all()
        for c in plan_claims:
            used_amount += c.amount
            
        remaining = travel_plan.approved_budget - used_amount
        
        if amount > remaining:
            return False, f"Insufficient travel budget. Remaining: {remaining}, Requested: {amount}", remaining
            
        return True, "Budget available", remaining

    else:
        # Non-travel claims (e.g. Team Lunch, Office Supplies)
        # For now, let's just check a global budget or return True if no specific budget linked
        # In a full app, user would select "Project X" from a dropdown
        return True, "Budget check skipped for non-travel (Project selection not implemented)", 999999.0
