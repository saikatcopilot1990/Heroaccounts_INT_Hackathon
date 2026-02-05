"""
Quick script to test email sending with actual database users.
"""
import sys
sys.path.insert(0, '.')

from app.db import SessionLocal
from app.models import User
from app.services import notify

# Get a database session
db = SessionLocal()

try:
    # Get all users
    users = db.query(User).all()
    
    print("=" * 60)
    print("DATABASE USERS:")
    print("=" * 60)
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}, Role: {user.role.value}")
    
    if users:
        print("\n" + "=" * 60)
        print("TESTING EMAIL NOTIFICATION")
        print("=" * 60)
        
        # Get the first user to test with
        test_user = users[0]
        print(f"\nSending test email to: {test_user.name} ({test_user.email})")
        
        # Try sending a notification
        success = notify.notify_status_change(
            user=test_user,
            claim_id=99999,
            status="APPROVED",
            comments="This is a test notification to verify email is working."
        )
        
        if success:
            print("\n✓ Email sent successfully!")
            print(f"Check {test_user.email} inbox for the test email.")
        else:
            print("\n✗ Email sending failed. Check SMTP configuration.")
    else:
        print("\nNo users found in database. Please seed the database first.")
        
finally:
    db.close()

print("\n" + "=" * 60)
