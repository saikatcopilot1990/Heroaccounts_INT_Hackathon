"""
Test Script for Email Notification System

Tests the HTML and text email functionality with sample data.
This script allows you to verify email templates without needing
to trigger actual claim workflows.
"""

import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services import html_mail, text_mail
from app.config import get_settings

settings = get_settings()


def test_html_templates():
    """Test HTML email template generation."""
    print("=" * 60)
    print("TESTING HTML EMAIL TEMPLATES")
    print("=" * 60)
    
    # Test 1: Status Change Email
    print("\n1. Testing Status Change HTML Template...")
    html_status = html_mail.create_status_change_html(
        user_name="John Doe",
        claim_id=12345,
        status="APPROVED",
        comments="All receipts verified. Payment will be processed within 2 business days.",
        dashboard_url=settings.app_url
    )
    
    # Save to file for inspection
    with open("test_status_change.html", "w", encoding="utf-8") as f:
        f.write(html_status)
    print("   ✓ Status change HTML generated and saved to test_status_change.html")
    
    # Test 2: Approver Notification Email
    print("\n2. Testing Approver Notification HTML Template...")
    html_approver = html_mail.create_approver_notification_html(
        approver_name="Jane Manager",
        claim_id=12345,
        submitter_name="John Doe",
        amount=2500.00,
        category="Travel",
        dashboard_url=settings.app_url
    )
    
    # Save to file for inspection
    with open("test_approver_notification.html", "w", encoding="utf-8") as f:
        f.write(html_approver)
    print("   ✓ Approver notification HTML generated and saved to test_approver_notification.html")


def test_text_templates():
    """Test plain text email template generation."""
    print("\n" + "=" * 60)
    print("TESTING PLAIN TEXT EMAIL TEMPLATES")
    print("=" * 60)
    
    # Test 1: Status Change Email
    print("\n1. Testing Status Change Text Template...")
    text_status = text_mail.create_status_change_text(
        user_name="John Doe",
        claim_id=12345,
        status="APPROVED",
        comments="All receipts verified. Payment will be processed within 2 business days.",
        dashboard_url=settings.app_url
    )
    
    # Save to file for inspection
    with open("test_status_change.txt", "w", encoding="utf-8") as f:
        f.write(text_status)
    print("   ✓ Status change text generated and saved to test_status_change.txt")
    print("\n   Preview:")
    print("   " + "-" * 56)
    for line in text_status.split("\n")[:15]:  # Show first 15 lines
        print("   " + line)
    print("   ...")
    
    # Test 2: Approver Notification Email
    print("\n2. Testing Approver Notification Text Template...")
    text_approver = text_mail.create_approver_notification_text(
        approver_name="Jane Manager",
        claim_id=12345,
        submitter_name="John Doe",
        amount=2500.00,
        category="Travel",
        dashboard_url=settings.app_url
    )
    
    # Save to file for inspection
    with open("test_approver_notification.txt", "w", encoding="utf-8") as f:
        f.write(text_approver)
    print("   ✓ Approver notification text generated and saved to test_approver_notification.txt")


def test_email_sending():
    """Test actual email sending (requires SMTP configuration)."""
    print("\n" + "=" * 60)
    print("TESTING EMAIL SENDING")
    print("=" * 60)
    
    if not settings.smtp_user or not settings.smtp_pass:
        print("\n⚠️  WARNING: SMTP credentials not configured in .env file")
        print("   To test actual email sending, please configure:")
        print("   - smtp_host (default: smtp.gmail.com)")
        print("   - smtp_port (default: 587)")
        print("   - smtp_user (your email)")
        print("   - smtp_pass (your app password)")
        print("\n   Skipping email sending test.")
        return
    
    print(f"\n📧 SMTP Configuration:")
    print(f"   Host: {settings.smtp_host}")
    print(f"   Port: {settings.smtp_port}")
    print(f"   User: {settings.smtp_user}")
    print(f"   Email Format: {settings.email_format}")
    
    # Ask user if they want to send test email
    response = input("\n   Send a test email to yourself? (y/n): ")
    if response.lower() != 'y':
        print("   Skipping email sending test.")
        return
    
    # Import notify module
    from app.services import notify
    
    # Create a mock user object
    class MockUser:
        def __init__(self, name, email):
            self.name = name
            self.email = email
    
    test_user = MockUser(
        name=input("   Enter recipient name: "),
        email=input("   Enter recipient email: ")
    )
    
    print("\n   Sending test email...")
    success = notify.send_email(
        to_email=test_user.email,
        subject="Hero Accounts - Test Email",
        body=text_mail.create_status_change_text(
            user_name=test_user.name,
            claim_id=99999,
            status="APPROVED",
            comments="This is a test email from the Hero Accounts system.",
            dashboard_url=settings.app_url
        ),
        html_body=html_mail.create_status_change_html(
            user_name=test_user.name,
            claim_id=99999,
            status="APPROVED",
            comments="This is a test email from the Hero Accounts system.",
            dashboard_url=settings.app_url
        )
    )
    
    if success:
        print("\n   ✓ Test email sent successfully!")
        print(f"   Check {test_user.email} for the email.")
    else:
        print("\n   ✗ Failed to send test email. Check SMTP configuration.")


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "HERO ACCOUNTS EMAIL SYSTEM TEST" + " " * 16 + "║")
    print("╚" + "=" * 58 + "╝")
    
    test_html_templates()
    test_text_templates()
    test_email_sending()
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - test_status_change.html")
    print("  - test_status_change.txt")
    print("  - test_approver_notification.html")
    print("  - test_approver_notification.txt")
    print("\nYou can open the HTML files in a browser to preview the emails.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
