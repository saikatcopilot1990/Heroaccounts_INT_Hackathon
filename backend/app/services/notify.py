"""
Notification Service Module

Handles email notifications for the Hero Accounts system.
Integrates html_mail and text_mail modules for rich email support.
"""

import smtplib
from email.message import EmailMessage
from typing import Optional

from app.config import get_settings
from app.models import User
from app.services import html_mail, text_mail

settings = get_settings()


def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None
) -> bool:
    """
    Sends an email using the configured SMTP server.
    
    Supports both plain text and HTML emails. If html_body is provided and
    email_format allows HTML, sends a multipart email with both versions.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text email body
        html_body: Optional HTML email body
    
    Returns:
        True if email was sent successfully, False otherwise
    """
    if not settings.smtp_host or not settings.smtp_user:
        print("SMTP not configured. Skipping email.")
        return False

    try:
        # Determine if we should send HTML
        send_html = (
            html_body is not None and 
            settings.email_format in ["html", "both"]
        )
        
        if send_html:
            # Create multipart message with both HTML and text
            msg = html_mail.create_html_email(
                to_email=to_email,
                subject=subject,
                html_content=html_body,
                text_content=body,
                from_email=settings.smtp_user
            )
        else:
            # Create plain text message
            msg = EmailMessage()
            msg.set_content(body)
            msg["Subject"] = subject
            msg["From"] = settings.smtp_user
            msg["To"] = to_email
        
        # Send the email
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_pass)
            server.send_message(msg)
        
        print(f"✓ Email sent to {to_email} (format: {'HTML+Text' if send_html else 'Text only'})")
        return True
        
    except Exception as e:
        print(f"✗ Failed to send email to {to_email}: {e}")
        return False


def notify_status_change(
    user: User,
    claim_id: int,
    status: str,
    comments: Optional[str] = None
) -> bool:
    """
    Sends a notification to the user about a claim status change.
    
    Args:
        user: User object receiving the notification
        claim_id: ID of the claim
        status: New status of the claim
        comments: Optional comments from the approver
    
    Returns:
        True if notification was sent successfully, False otherwise
    """
    subject = f"Claim #{claim_id} Status Update: {status}"
    
    # Generate plain text version
    text_body = text_mail.create_status_change_text(
        user_name=user.name,
        claim_id=claim_id,
        status=status,
        comments=comments,
        dashboard_url=settings.app_url
    )
    
    # Generate HTML version
    html_body = html_mail.create_status_change_html(
        user_name=user.name,
        claim_id=claim_id,
        status=status,
        comments=comments,
        dashboard_url=settings.app_url
    )
    
    return send_email(user.email, subject, text_body, html_body)


def notify_approver(
    approver: User,
    claim_id: int,
    submitter_name: str,
    amount: Optional[float] = None,
    category: Optional[str] = None
) -> bool:
    """
    Notifies an approver that a new claim is pending their action.
    
    Args:
        approver: User object of the approver
        claim_id: ID of the claim
        submitter_name: Name of the person who submitted the claim
        amount: Optional claim amount
        category: Optional claim category
    
    Returns:
        True if notification was sent successfully, False otherwise
    """
    subject = f"Action Required: Claim #{claim_id} from {submitter_name}"
    
    # Generate plain text version
    text_body = text_mail.create_approver_notification_text(
        approver_name=approver.name,
        claim_id=claim_id,
        submitter_name=submitter_name,
        amount=amount,
        category=category,
        dashboard_url=settings.app_url
    )
    
    # Generate HTML version
    html_body = html_mail.create_approver_notification_html(
        approver_name=approver.name,
        claim_id=claim_id,
        submitter_name=submitter_name,
        amount=amount,
        category=category,
        dashboard_url=settings.app_url
    )
    
    return send_email(approver.email, subject, text_body, html_body)


def send_generic_notification(
    user: User,
    subject: str,
    message: str
) -> bool:
    """
    Sends a generic notification email to a user.
    
    Args:
        user: User object receiving the notification
        subject: Email subject
        message: Email message content
    
    Returns:
        True if notification was sent successfully, False otherwise
    """
    # Generate plain text version
    text_body = text_mail.create_generic_text(
        recipient_name=user.name,
        subject=subject,
        message=message,
        dashboard_url=settings.app_url
    )
    
    # For generic notifications, we'll use simple text
    # Could be enhanced to support HTML if needed
    return send_email(user.email, subject, text_body)

