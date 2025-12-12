import enum
from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Boolean,
    Text
)
from sqlalchemy.orm import relationship
from .db import Base

class UserRole(str, enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    FINANCE = "finance"
    ADMIN = "admin"

class ClaimStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED_BY_MANAGER = "approved_by_manager"
    APPROVED_BY_FINANCE = "approved_by_finance"
    REJECTED = "rejected"
    PAID = "paid"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    manager = relationship("User", remote_side=[id], backref="subordinates")
    claims = relationship("Claim", back_populates="employee", foreign_keys="Claim.employee_id")
    approvals = relationship("Approval", back_populates="approver")
    notifications = relationship("Notification", back_populates="user")

class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    estimated_budget = Column(Float, nullable=False)
    approved_budget = Column(Float, nullable=True)
    status = Column(String, default="approved") # simplified for now
    
    # Relationships
    employee = relationship("User", backref="travel_plans")
    claims = relationship("Claim", back_populates="travel_plan")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # e.g., "Project X", "Marketing Q1"
    total_amount = Column(Float, nullable=False)
    used_amount = Column(Float, default=0.0)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    claims = relationship("Claim", back_populates="budget")

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    travel_plan_id = Column(Integer, ForeignKey("travel_plans.id"), nullable=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=True)
    
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    vendor = Column(String, nullable=True)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    gst_number = Column(String, nullable=True)
    
    status = Column(Enum(ClaimStatus), default=ClaimStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("User", back_populates="claims", foreign_keys=[employee_id])
    travel_plan = relationship("TravelPlan", back_populates="claims")
    budget = relationship("Budget", back_populates="claims")
    receipt = relationship("Receipt", uselist=False, back_populates="claim")
    approvals = relationship("Approval", back_populates="claim")

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=True)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    extracted_text = Column(Text, nullable=True)
    extracted_data = Column(JSON, nullable=True) # Full JSON from extraction
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    claim = relationship("Claim", back_populates="receipt")

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, nullable=False) # manager, finance
    status = Column(String, nullable=False) # approved, rejected
    comments = Column(Text, nullable=True)
    decided_at = Column(DateTime, default=datetime.utcnow)
    
    claim = relationship("Claim", back_populates="approvals")
    approver = relationship("User", back_populates="approvals")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="notifications")
