"""
Update employee email addresses to vikas@intglobal.com for testing
"""
import sys
sys.path.insert(0, '.')

from app.db import SessionLocal
from app.models import User, UserRole

db = SessionLocal()

try:
    print("=" * 70)
    print("CURRENT USERS:")
    print("=" * 70)
    users = db.query(User).all()
    for user in users:
        print(f"ID: {user.id} | Name: {user.name:20s} | Email: {user.email:35s} | Role: {user.role.value}")
    
    # Update employee emails to vikas@intglobal.com
    print("\n" + "=" * 70)
    print("UPDATING EMPLOYEE EMAILS TO vikas@intglobal.com")
    print("=" * 70)
    
    employees = db.query(User).filter(User.role == UserRole.EMPLOYEE).all()
    
    for emp in employees:
        old_email = emp.email
        emp.email = "vikas@intglobal.com"
        print(f"Updated: {emp.name:20s} | {old_email:35s} -> vikas@intglobal.com")
    
    db.commit()
    
    print("\n" + "=" * 70)
    print("UPDATED USERS:")
    print("=" * 70)
    users = db.query(User).all()
    for user in users:
        print(f"ID: {user.id} | Name: {user.name:20s} | Email: {user.email:35s} | Role: {user.role.value}")
    
    print("\n" + "=" * 70)
    print("✓ Email addresses updated successfully!")
    print("=" * 70)
    print("\nNow when you approve claims, notifications will be sent to vikas@intglobal.com")
    
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()
