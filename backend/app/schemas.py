from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ClaimBase(BaseModel):
    amount: float
    date: str
    vendor: Optional[str] = None
    category: str
    description: Optional[str] = None
    gst: Optional[str] = None

class ClaimCreate(ClaimBase):
    employee_id: int # In real app, get from auth token

class ClaimResponse(ClaimBase):
    id: int
    status: str
    is_valid: bool = True
    validation_message: Optional[str] = None
    budget_remaining: Optional[float] = None

class ApprovalRequest(BaseModel):
    claim_id: int
    approver_id: int
    action: str # approve, reject
    comments: Optional[str] = None

class NotificationRequest(BaseModel):
    user_id: int
    message: str

class SyncSheetRequest(BaseModel):
    claim_id: int

