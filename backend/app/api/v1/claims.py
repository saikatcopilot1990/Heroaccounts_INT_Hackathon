from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional
import shutil
import os
from datetime import datetime

from app.db import SessionLocal
from app.models import Claim, Receipt, User, ClaimStatus
from app.schemas import ClaimResponse, ApprovalRequest
from app.services import extraction, policy, budget, workflow, notify, reporting

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload-receipt")
async def upload_receipt(
    file: UploadFile = File(...),
    # employee_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Uploads a receipt PDF, extracts data, and creates a Draft Claim.
    """
    # Save file
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = f"{upload_dir}/{datetime.now().timestamp()}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract Data
    extraction_result = extraction.receipt_to_json(file_path)
    extracted_data = extraction_result["extracted_data"]
    
    # Create Claim (Draft)
    # Note: In a real app, we'd validate the extracted data first or let user edit it.
    # Here we assume auto-creation for simplicity, or we return data for user to confirm.
    # Let's return the data so frontend can populate the form.
    
    # We also save the receipt record
    receipt = Receipt(
        file_path=file_path,
        file_name=file.filename,
        extracted_text=extraction_result["raw_text"],
        extracted_data=extracted_data
    )
    print("Extracted Data:", extracted_data)
    # db.add(receipt)
    # db.commit()
    # db.refresh(receipt)
     # DELETE THE FILE AFTER PROCESSING
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted uploaded file: {file_path}")
    return {
        "receipt_id": receipt.id,
        "extracted_data": extracted_data,
        "message": "Receipt uploaded and processed. Please review and submit claim."
    }
def parse_date(date_str: str):
    formats = [
        "%Y-%m-%d",    # 2025-02-12
        "%d-%m-%Y",    # 12-02-2025
        "%d-%b-%Y",    # 12-Feb-2025
        "%d/%m/%Y",    # 12/02/2025
        "%d/%b/%Y",    # 12/Feb/2025
        "%d %b %Y",    # 12 Feb 2025
        "%b %d, %Y",   # Feb 12, 2025
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except:
            pass
    raise ValueError(f"Invalid date format: {date_str}")

@router.post("/submit-claim")
async def submit_claim(
    claim_data: dict,
    db: Session = Depends(get_db)
):
    """
    Validates, Checks Budget, and Submits a Claim.
    """
    employee_id = claim_data.get("employee_id")
    receipt_id = claim_data.get("receipt_id")
    
    # 1. Policy Validation
    is_valid, val_msg = policy.validate_claim(db, claim_data, employee_id)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Policy Violation: {val_msg}")
        
    # 2. Budget Check
    is_eligible, bud_msg, remaining = budget.check_budget(db, claim_data, employee_id)
    if not is_eligible:
        raise HTTPException(status_code=400, detail=f"Budget Issue: {bud_msg}")
        
    # 3. Create/Update Claim Record
    # If we already created a draft, we update it. Here we create new for simplicity if not exists.
    
    claim = Claim(
        employee_id=employee_id,
        amount=float(claim_data.get("amount")),
        date=parse_date(claim_data.get("date")),
        vendor=claim_data.get("vendor"),
        category=claim_data.get("category"),
        purpose=claim_data.get("purpose"),
        gst_number=claim_data.get("gst"),
        status=ClaimStatus.SUBMITTED
    )
    db.add(claim)
    db.commit()
    
    # Link Receipt
    if receipt_id:
        receipt = db.query(Receipt).get(receipt_id)
        if receipt:
            receipt.claim_id = claim.id
            db.commit()
            
    # 4. Notify Manager
    employee = db.query(User).get(employee_id)
    if employee and employee.manager:
        notify.notify_approver(employee.manager, claim.id, employee.name)
        
    return {"message": "Claim submitted successfully", "claim_id": claim.id}

@router.post("/approve-claim")
async def approve_claim_endpoint(
    request: ApprovalRequest,
    db: Session = Depends(get_db)
):
    """
    Approves or Rejects a claim.
    """
    if request.action == "approve":
        success, msg = workflow.approve_claim(db, request.claim_id, request.approver_id, request.comments)
        if success:
            # Check if fully approved (Paid/Approved by Finance)
            claim = db.query(Claim).get(request.claim_id)
            if claim.status == ClaimStatus.APPROVED_BY_FINANCE:
                # Sync to Sheet
                reporting.update_excel_ledger(claim)
                # Notify Employee
                notify.notify_status_change(claim.employee, claim.id, "Approved by Finance", request.comments)
            elif claim.status == ClaimStatus.APPROVED_BY_MANAGER:
                 # Notify Finance (find finance user)
                 # For demo, just notify employee of progress
                 notify.notify_status_change(claim.employee, claim.id, "Approved by Manager", request.comments)
                 
        else:
            raise HTTPException(status_code=400, detail=msg)
            
    elif request.action == "reject":
        success, msg = workflow.reject_claim(db, request.claim_id, request.approver_id, request.comments)
        if success:
            claim = db.query(Claim).get(request.claim_id)
            notify.notify_status_change(claim.employee, claim.id, "Rejected", request.comments)
        else:
            raise HTTPException(status_code=400, detail=msg)
            
    return {"message": msg}

@router.get("/claims")
async def list_claims(db: Session = Depends(get_db)):
    """
    List all claims with employee and status information.
    """
    claims = db.query(Claim).all()
    
    claims_list = []
    for claim in claims:
        claims_list.append({
            "id": claim.id,
            "employee": claim.employee.name if claim.employee else "Unknown",
            "amount": claim.amount,
            "date": claim.date.strftime("%Y-%m-%d"),
            "vendor": claim.vendor,
            "category": claim.category,
            "status": claim.status.value,
            "created_at": claim.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return claims_list

@router.get("/claims/{claim_id}")
async def get_claim(claim_id: int, db: Session = Depends(get_db)):
    claim = db.query(Claim).get(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
