"""
HTML Email Template Module

Provides professional HTML email templates for the Hero Accounts system.
Includes templates for claim status updates and approver notifications.
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional


def get_email_header() -> str:
    """Returns the standard HTML email header with styling."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Accounts Notification</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7fa;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f7fa; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600;">Hero Accounts</h1>
                            <p style="margin: 5px 0 0 0; color: #e0e7ff; font-size: 14px;">Receipt & Reimbursement System</p>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
"""


def get_email_footer(dashboard_url: str = "http://localhost:5173") -> str:
    """Returns the standard HTML email footer."""
    return f"""
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-radius: 0 0 8px 8px; border-top: 1px solid #e9ecef;">
                            <p style="margin: 0 0 15px 0; font-size: 14px; color: #6c757d;">
                                Need help? Contact our support team.
                            </p>
                            <a href="{dashboard_url}" style="display: inline-block; padding: 12px 30px; background-color: #667eea; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: 500; margin-bottom: 15px;">
                                Go to Dashboard
                            </a>
                            <p style="margin: 15px 0 0 0; font-size: 12px; color: #adb5bd;">
                                © 2024 Hero Accounts. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""


def create_status_change_html(
    user_name: str,
    claim_id: int,
    status: str,
    comments: Optional[str] = None,
    dashboard_url: str = "http://localhost:5173"
) -> str:
    """
    Creates an HTML email template for claim status change notifications.
    
    Args:
        user_name: Name of the user receiving the notification
        claim_id: ID of the claim
        status: New status of the claim
        comments: Optional comments from the approver
        dashboard_url: URL to the dashboard
    
    Returns:
        Complete HTML email content
    """
    # Status color mapping
    status_colors = {
        "APPROVED": "#28a745",
        "REJECTED": "#dc3545",
        "PENDING": "#ffc107",
        "DRAFT": "#6c757d",
        "SUBMITTED": "#17a2b8"
    }
    
    status_color = status_colors.get(status.upper(), "#667eea")
    
    comments_section = ""
    if comments:
        comments_section = f"""
                            <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 15px; margin: 20px 0; border-radius: 4px;">
                                <p style="margin: 0; font-weight: 600; color: #495057; font-size: 14px;">Comments:</p>
                                <p style="margin: 10px 0 0 0; color: #6c757d; font-size: 14px; line-height: 1.6;">{comments}</p>
                            </div>
"""
    
    content = f"""
                            <h2 style="margin: 0 0 10px 0; color: #212529; font-size: 24px;">Claim Status Update</h2>
                            <p style="margin: 0 0 30px 0; color: #6c757d; font-size: 16px;">Hello {user_name},</p>
                            
                            <div style="background-color: #f8f9fa; padding: 25px; border-radius: 6px; margin-bottom: 25px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #6c757d; font-size: 14px;">Claim ID:</span>
                                        </td>
                                        <td style="padding: 8px 0; text-align: right;">
                                            <span style="color: #212529; font-weight: 600; font-size: 16px;">#{claim_id}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #6c757d; font-size: 14px;">New Status:</span>
                                        </td>
                                        <td style="padding: 8px 0; text-align: right;">
                                            <span style="background-color: {status_color}; color: #ffffff; padding: 6px 12px; border-radius: 4px; font-weight: 600; font-size: 14px; display: inline-block;">
                                                {status.upper()}
                                            </span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            
{comments_section}
                            
                            <p style="margin: 25px 0 0 0; color: #6c757d; font-size: 14px; line-height: 1.6;">
                                Please log in to your dashboard to view complete details and take any necessary actions.
                            </p>
"""
    
    return get_email_header() + content + get_email_footer(dashboard_url)


def create_approver_notification_html(
    approver_name: str,
    claim_id: int,
    submitter_name: str,
    amount: Optional[float] = None,
    category: Optional[str] = None,
    dashboard_url: str = "http://localhost:5173"
) -> str:
    """
    Creates an HTML email template for approver notifications.
    
    Args:
        approver_name: Name of the approver
        claim_id: ID of the claim
        submitter_name: Name of the person who submitted the claim
        amount: Optional claim amount
        category: Optional claim category
        dashboard_url: URL to the dashboard
    
    Returns:
        Complete HTML email content
    """
    amount_section = ""
    if amount is not None:
        amount_section = f"""
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #6c757d; font-size: 14px;">Amount:</span>
                                        </td>
                                        <td style="padding: 8px 0; text-align: right;">
                                            <span style="color: #212529; font-weight: 600; font-size: 16px;">₹{amount:,.2f}</span>
                                        </td>
                                    </tr>
"""
    
    category_section = ""
    if category:
        category_section = f"""
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #6c757d; font-size: 14px;">Category:</span>
                                        </td>
                                        <td style="padding: 8px 0; text-align: right;">
                                            <span style="color: #212529; font-weight: 500; font-size: 14px;">{category}</span>
                                        </td>
                                    </tr>
"""
    
    content = f"""
                            <h2 style="margin: 0 0 10px 0; color: #212529; font-size: 24px;">
                                <span style="color: #dc3545;">⚠️</span> Action Required
                            </h2>
                            <p style="margin: 0 0 30px 0; color: #6c757d; font-size: 16px;">Hello {approver_name},</p>
                            
                            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin-bottom: 25px; border-radius: 4px;">
                                <p style="margin: 0; color: #856404; font-size: 16px; font-weight: 600;">
                                    A new reimbursement claim requires your approval.
                                </p>
                            </div>
                            
                            <div style="background-color: #f8f9fa; padding: 25px; border-radius: 6px; margin-bottom: 25px;">
                                <table width="100%" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #6c757d; font-size: 14px;">Claim ID:</span>
                                        </td>
                                        <td style="padding: 8px 0; text-align: right;">
                                            <span style="color: #212529; font-weight: 600; font-size: 16px;">#{claim_id}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 8px 0;">
                                            <span style="color: #6c757d; font-size: 14px;">Submitted By:</span>
                                        </td>
                                        <td style="padding: 8px 0; text-align: right;">
                                            <span style="color: #212529; font-weight: 500; font-size: 14px;">{submitter_name}</span>
                                        </td>
                                    </tr>
{amount_section}{category_section}
                                </table>
                            </div>
                            
                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{dashboard_url}/claims/{claim_id}" style="display: inline-block; padding: 14px 35px; background-color: #28a745; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: 600; font-size: 16px;">
                                    Review & Approve
                                </a>
                            </div>
                            
                            <p style="margin: 25px 0 0 0; color: #6c757d; font-size: 14px; line-height: 1.6; text-align: center;">
                                Please review this claim at your earliest convenience.
                            </p>
"""
    
    return get_email_header() + content + get_email_footer(dashboard_url)


def create_html_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str,
    from_email: str
) -> MIMEMultipart:
    """
    Creates a MIME multipart email message with both HTML and plain text versions.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML version of the email
        text_content: Plain text version of the email
        from_email: Sender email address
    
    Returns:
        MIMEMultipart message ready to send
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    # Attach plain text version (should be first)
    part_text = MIMEText(text_content, 'plain')
    msg.attach(part_text)
    
    # Attach HTML version (should be second, preferred by email clients)
    part_html = MIMEText(html_content, 'html')
    msg.attach(part_html)
    
    return msg
