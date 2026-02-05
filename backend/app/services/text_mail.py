"""
Plain Text Email Template Module

Provides plain text email templates for the Hero Accounts system.
These serve as fallbacks for email clients that don't support HTML.
"""

from typing import Optional


def create_status_change_text(
    user_name: str,
    claim_id: int,
    status: str,
    comments: Optional[str] = None,
    dashboard_url: str = "http://localhost:5173"
) -> str:
    """
    Creates a plain text email template for claim status change notifications.
    
    Args:
        user_name: Name of the user receiving the notification
        claim_id: ID of the claim
        status: New status of the claim
        comments: Optional comments from the approver
        dashboard_url: URL to the dashboard
    
    Returns:
        Plain text email content
    """
    separator = "=" * 60
    
    comments_section = ""
    if comments:
        comments_section = f"""
COMMENTS:
{comments}

{separator}
"""
    
    text = f"""
{separator}
           HERO ACCOUNTS - CLAIM STATUS UPDATE
{separator}

Hello {user_name},

Your reimbursement claim has been updated.

CLAIM DETAILS:
--------------
Claim ID:       #{claim_id}
New Status:     {status.upper()}

{comments_section}
Please log in to your dashboard to view complete details and take
any necessary actions.

Dashboard: {dashboard_url}

{separator}

If you have any questions, please contact our support team.

Regards,
Hero Accounts Team

© 2024 Hero Accounts. All rights reserved.
"""
    
    return text.strip()


def create_approver_notification_text(
    approver_name: str,
    claim_id: int,
    submitter_name: str,
    amount: Optional[float] = None,
    category: Optional[str] = None,
    dashboard_url: str = "http://localhost:5173"
) -> str:
    """
    Creates a plain text email template for approver notifications.
    
    Args:
        approver_name: Name of the approver
        claim_id: ID of the claim
        submitter_name: Name of the person who submitted the claim
        amount: Optional claim amount
        category: Optional claim category
        dashboard_url: URL to the dashboard
    
    Returns:
        Plain text email content
    """
    separator = "=" * 60
    
    amount_section = ""
    if amount is not None:
        amount_section = f"Amount:         ₹{amount:,.2f}\n"
    
    category_section = ""
    if category:
        category_section = f"Category:       {category}\n"
    
    text = f"""
{separator}
        HERO ACCOUNTS - ACTION REQUIRED
{separator}

⚠️ APPROVAL NEEDED

Hello {approver_name},

A new reimbursement claim has been submitted and requires your approval.

CLAIM DETAILS:
--------------
Claim ID:       #{claim_id}
Submitted By:   {submitter_name}
{amount_section}{category_section}
Status:         PENDING APPROVAL

{separator}

Please log in to the dashboard to review and approve/reject this claim
at your earliest convenience.

Dashboard: {dashboard_url}/claims/{claim_id}

Direct action link: {dashboard_url}

{separator}

If you have any questions, please contact our support team.

Regards,
Hero Accounts Team

© 2024 Hero Accounts. All rights reserved.
"""
    
    return text.strip()


def create_generic_text(
    recipient_name: str,
    subject: str,
    message: str,
    dashboard_url: str = "http://localhost:5173"
) -> str:
    """
    Creates a generic plain text email template.
    
    Args:
        recipient_name: Name of the recipient
        subject: Email subject/title
        message: Main message content
        dashboard_url: URL to the dashboard
    
    Returns:
        Plain text email content
    """
    separator = "=" * 60
    
    text = f"""
{separator}
           HERO ACCOUNTS - {subject.upper()}
{separator}

Hello {recipient_name},

{message}

{separator}

Dashboard: {dashboard_url}

If you have any questions, please contact our support team.

Regards,
Hero Accounts Team

© 2024 Hero Accounts. All rights reserved.
"""
    
    return text.strip()
