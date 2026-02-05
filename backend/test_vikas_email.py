"""
Direct email test to vikas@intglobal.com
"""
import sys
sys.path.insert(0, '.')

from app.db import SessionLocal
from app.models import User, Claim
from app.services import notify

db = SessionLocal()

try:
    # Get all users and their emails
    print("=" * 70)
    print("DATABASE USERS AND EMAILS:")
    print("=" * 70)
    users = db.query(User).all()
    for user in users:
        print(f"ID: {user.id} | Name: {user.name:20s} | Email: {user.email:35s} | Role: {user.role.value}")
    
    # Find user with vikas@intglobal.com
    vikas_user = db.query(User).filter(User.email == "vikas@intglobal.com").first()
    
    print("\n" + "=" * 70)
    if vikas_user:
        print(f"✓ Found user with vikas@intglobal.com: {vikas_user.name}")
        
        # Send test email
        print("\nSending test email to vikas@intglobal.com...")
        success = notify.notify_status_change(
            user=vikas_user,
            claim_id=12345,
            status="APPROVED",
            comments="This is a DIRECT test email to verify you can receive emails."
        )
        
        if success:
            print("✓ Email sent successfully!")
            print("\nPlease check:")
            print("  1. Inbox at vikas@intglobal.com")
            print("  2. Spam/Junk folder")
            print("  3. All Mail folder (in Gmail)")
        else:
            print("✗ Failed to send email")
    else:
        print("✗ No user found with email vikas@intglobal.com")
        print("\nAvailable email addresses:")
        for user in users:
            print(f"  - {user.email}")
    
    # Check actual claims and their employee emails
    print("\n" + "=" * 70)
    print("RECENT CLAIMS AND EMPLOYEE EMAILS:")
    print("=" * 70)
    claims = db.query(Claim).order_by(Claim.id.desc()).limit(5).all()
    for claim in claims:
        if claim.employee:
            print(f"Claim #{claim.id} | Status: {claim.status.value:25s} | Employee: {claim.employee.name:20s} ({claim.employee.email})")
        else:
            print(f"Claim #{claim.id} | Status: {claim.status.value:25s} | Employee: No employee assigned")
            
finally:
    db.close()

print("\n" + "=" * 70)
