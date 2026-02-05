"""
Final comprehensive email test
"""
import sys
sys.path.insert(0, '.')

from app.services import notify
from app.models import User
from app.db import SessionLocal

class TestUser:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# Create test user
test_user = TestUser("Vikas Test", "vikas@intglobal.com")

print("=" * 70)
print("SENDING TEST EMAIL TO: vikas@intglobal.com")
print("=" * 70)

# Send test notification
print("\nSending email...")
result = notify.notify_status_change(
    user=test_user,
    claim_id=99999,
    status="APPROVED",
    comments="✅ This is a TEST EMAIL from Hero Accounts system. If you receive this, email notifications are working perfectly!"
)

if result:
    print("\n✅ SUCCESS! Email sent to vikas@intglobal.com")
    print("\nPlease check your email inbox:")
    print("  1. Primary inbox")
    print("  2. Spam/Junk folder")
    print("  3. Promotions tab (if using Gmail)")
    print("  4. All Mail")
    print("\nLook for subject: 'Claim #99999 Status Update: APPROVED'")
else:
    print("\n❌ FAILED to send email")
    print("Check SMTP configuration")

print("\n" + "=" * 70)

# Also check database
print("\nDATABASE CHECK:")
print("=" * 70)
db = SessionLocal()
try:
    users_with_vikas = db.query(User).filter(User.email == "vikas@intglobal.com").all()
    if users_with_vikas:
        print(f"✓ Found {len(users_with_vikas)} user(s) with vikas@intglobal.com:")
        for u in users_with_vikas:
            print(f"  - {u.name} (ID: {u.id}, Role: {u.role.value})")
    else:
        print("✗ No users found with vikas@intglobal.com in database")
finally:
    db.close()

print("=" * 70)
