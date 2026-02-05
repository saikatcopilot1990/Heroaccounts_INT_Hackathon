"""
Check database users and their email addresses for claims.
"""
import sys
sys.path.insert(0, '.')

from app.db import SessionLocal
from app.models import User, Claim
from sqlalchemy.orm import joinedload

# Get a database session
db = SessionLocal()

try:
    print("=" * 70)
    print("ALL USERS IN DATABASE:")
    print("=" * 70)
    users = db.query(User).all()
    for user in users:
        print(f"ID: {user.id:2d} | Name: {user.name:20s} | Email: {user.email:30s} | Role: {user.role.value}")
    
    print("\n" + "=" * 70)
    print("ALL CLAIMS WITH EMPLOYEE DETAILS:")
    print("=" * 70)
    claims = db.query(Claim).options(joinedload(Claim.employee)).all()
    
    if not claims:
        print("No claims found in database.")
    else:
        for claim in claims:
            employee_email = claim.employee.email if claim.employee else "NO EMPLOYEE"
            print(f"Claim ID: {claim.id:3d} | Amount: ₹{claim.amount:8.2f} | Status: {claim.status.value:20s}")
            print(f"           Employee: {claim.employee.name if claim.employee else 'Unknown':20s} | Email: {employee_email}")
            print("-" * 70)
    
finally:
    db.close()
