from sqlalchemy.orm import Session
from app.models import Claim, ClaimStatus, Approval, User, UserRole
from datetime import datetime

def submit_claim(db: Session, claim: Claim):
    """
    Submits a claim for approval.
    Transition: DRAFT -> SUBMITTED (Pending Manager)
    """
    if claim.status != ClaimStatus.DRAFT:
        return False, "Claim is not in draft status."
    
    claim.status = ClaimStatus.SUBMITTED
    db.commit()
    return True, "Claim submitted successfully."

def approve_claim(db: Session, claim_id: int, approver_id: int, comments: str = None):
    """
    Approves a claim based on the approver's role.
    Transitions:
    - SUBMITTED (Manager) -> APPROVED_BY_MANAGER (Pending Finance)
    - APPROVED_BY_MANAGER (Finance) -> APPROVED_BY_FINANCE (Ready for Payment)
    """
    claim = db.query(Claim).get(claim_id)
    approver = db.query(User).get(approver_id)
    
    if not claim or not approver:
        return False, "Claim or Approver not found."

    # Check for invalid states first
    if claim.status == ClaimStatus.DRAFT:
        return False, "Cannot approve a draft claim. Please submit the claim first."
    
    if claim.status == ClaimStatus.REJECTED:
        return False, "Cannot approve a rejected claim."
    
    if claim.status == ClaimStatus.APPROVED_BY_FINANCE:
        return False, "Claim is already fully approved by Finance."
    
    if claim.status == ClaimStatus.PAID:
        return False, "Claim has already been paid."

    # Manager Approval
    if claim.status == ClaimStatus.SUBMITTED:
        # Verify if approver is the manager
        # (In strict mode, check if approver.id == claim.employee.manager_id)
        if approver.role != UserRole.MANAGER and approver.role != UserRole.ADMIN:
             return False, "Only managers can approve submitted claims."
        
        claim.status = ClaimStatus.APPROVED_BY_MANAGER
        
        # Log approval
        approval_record = Approval(
            claim_id=claim.id,
            approver_id=approver.id,
            role="manager",
            status="approved",
            comments=comments
        )
        db.add(approval_record)
        db.commit()
        return True, "Manager approved. Sent to Finance."

    # Finance Approval
    elif claim.status == ClaimStatus.APPROVED_BY_MANAGER:
        if approver.role != UserRole.FINANCE and approver.role != UserRole.ADMIN:
            return False, "Only finance team can approve this claim."
            
        claim.status = ClaimStatus.APPROVED_BY_FINANCE
        
        # Log approval
        approval_record = Approval(
            claim_id=claim.id,
            approver_id=approver.id,
            role="finance",
            status="approved",
            comments=comments
        )
        db.add(approval_record)
        db.commit()
        return True, "Finance approved. Ready for payment."

    # This should never be reached due to checks above, but keeping for safety
    return False, f"Invalid state for approval. Current status: {claim.status.value}"


def reject_claim(db: Session, claim_id: int, approver_id: int, comments: str):
    """
    Rejects a claim.
    Transition: ANY -> REJECTED
    """
    claim = db.query(Claim).get(claim_id)
    approver = db.query(User).get(approver_id)
    
    if not claim or not approver:
        return False, "Claim or Approver not found."
        
    claim.status = ClaimStatus.REJECTED
    
    # Log rejection
    approval_record = Approval(
        claim_id=claim.id,
        approver_id=approver.id,
        role=approver.role.value,
        status="rejected",
        comments=comments
    )
    db.add(approval_record)
    db.commit()
    return True, "Claim rejected."
