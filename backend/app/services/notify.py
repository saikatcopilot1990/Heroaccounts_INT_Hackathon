import smtplib
from email.message import EmailMessage
from app.config import get_settings
from app.models import User

settings = get_settings()

def send_email(to_email: str, subject: str, body: str):
    """
    Sends an email using the configured SMTP server.
    """
    if not settings.smtp_host or not settings.smtp_user:
        print("SMTP not configured. Skipping email.")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = settings.smtp_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_pass)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def notify_status_change(user: User, claim_id: int, status: str, comments: str = None):
    """
    Sends a notification to the user about a claim status change.
    """
    subject = f"Claim #{claim_id} Status Update: {status}"
    body = f"Hello {user.name},\n\nYour claim #{claim_id} has been updated to: {status}.\n"
    
    if comments:
        body += f"\nComments: {comments}\n"
        
    body += "\nPlease check the dashboard for more details.\n\nRegards,\nHero Accounts Team"
    
    send_email(user.email, subject, body)

def notify_approver(approver: User, claim_id: int, submitter_name: str):
    """
    Notifies an approver that a new claim is pending their action.
    """
    subject = f"Action Required: Claim #{claim_id} from {submitter_name}"
    body = f"Hello {approver.name},\n\nA new claim #{claim_id} from {submitter_name} is pending your approval.\n"
    body += "\nPlease log in to the dashboard to review and approve/reject.\n\nRegards,\nHero Accounts Team"
    
    send_email(approver.email, subject, body)
