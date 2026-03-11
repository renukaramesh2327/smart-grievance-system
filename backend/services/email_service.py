"""
Email Service with Formspree Integration
Supports: Gmail SMTP, Formspree API, and Console fallback
"""

from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠ 'requests' library not installed. Run: pip install requests")

from backend.config import Config

class EmailService:
    # Formspree endpoint (set via environment variable)
    FORMSPREE_ENDPOINT = os.environ.get('FORMSPREE_ENDPOINT', '')
    
    @staticmethod
    def send_via_gmail(to_email, subject, body):
        """
        Send email via Gmail SMTP
        """
        try:
            if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = Config.MAIL_DEFAULT_SENDER
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Create HTML version
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                        <div style="background: linear-gradient(135deg, #2563eb, #1e40af); color: white; padding: 20px; border-radius: 10px 10px 0 0; text-align: center;">
                            <h2 style="margin: 0;">🇮🇳 Smart Grievance System</h2>
                        </div>
                        <div style="padding: 20px; background: #f9fafb;">
                            <pre style="white-space: pre-wrap; font-family: Arial, sans-serif;">{body}</pre>
                        </div>
                        <div style="padding: 15px; background: #e5e7eb; text-align: center; font-size: 12px; color: #6b7280; border-radius: 0 0 10px 10px;">
                            <p style="margin: 0;">This is an automated message from Smart Grievance System</p>
                            <p style="margin: 5px 0 0 0;">Please do not reply to this email</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Attach both plain text and HTML
            part1 = MIMEText(body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                server.starttls()
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                server.send_message(msg)
            
            print(f"✓ Email sent via Gmail to {to_email}")
            return True
            
        except Exception as e:
            print(f"⚠ Gmail SMTP failed: {e}")
            return False
    
    @staticmethod
    def send_via_formspree(to_email, subject, body):
        """
        Send email via Formspree API (Free tier: 50 submissions/month)
        """
        if not REQUESTS_AVAILABLE:
            return False
            
        if not EmailService.FORMSPREE_ENDPOINT:
            return False
        
        try:
            response = requests.post(
                EmailService.FORMSPREE_ENDPOINT,
                data={
                    'email': to_email,
                    'subject': subject,
                    'message': body,
                    '_replyto': to_email,
                    '_subject': subject,
                    '_template': 'table'
                },
                headers={
                    'Accept': 'application/json'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✓ Email sent via Formspree to {to_email}")
                return True
            else:
                print(f"⚠ Formspree API error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"⚠ Formspree failed: {e}")
            return False
    
    @staticmethod
    def send_to_console(to_email, subject, body):
        """
        Fallback: Print email to console (Demo mode)
        """
        print(f"\n{'='*70}")
        print(f"📧 [EMAIL NOTIFICATION]")
        print(f"{'='*70}")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"{'='*70}")
        print(body)
        print(f"{'='*70}\n")
        return True
    
    @staticmethod
    def send_email(to_email, subject, body):
        """
        Smart email sending with multiple fallbacks:
        1. Try Gmail SMTP (if configured)
        2. Try Formspree (if configured)
        3. Fallback to console output
        """
        # Check if demo mode is explicitly enabled
        if Config.DEMO_EMAIL_MODE:
            return EmailService.send_to_console(to_email, subject, body)
        
        # Try Gmail first
        if Config.MAIL_USERNAME and Config.MAIL_PASSWORD:
            if EmailService.send_via_gmail(to_email, subject, body):
                return True
            print("→ Trying Formspree as backup...")
        
        # Try Formspree
        if EmailService.FORMSPREE_ENDPOINT:
            if EmailService.send_via_formspree(to_email, subject, body):
                return True
            print("→ Falling back to console output...")
        
        # Final fallback to console
        return EmailService.send_to_console(to_email, subject, body)
    
    @staticmethod
    def send_grievance_notification(user_email, grievance_id, department, status, message):
        """
        Send notification about grievance update
        """
        subject = f"Grievance #{grievance_id} - Status Update: {status}"
        
        # Create tracking URL
        tracking_url = f"http://localhost:8000/track.html?id={grievance_id}"
        
        body = f"""
Dear Citizen,

Your grievance has been updated:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 COMPLAINT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complaint ID: #{grievance_id}
Department: {department}
Current Status: {status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 UPDATE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 TRACK YOUR COMPLAINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{tracking_url}

Thank you for using the Smart Grievance System.

---
This is an automated message. Please do not reply.
Smart Grievance System | Digital India Initiative
        """
        
        return EmailService.send_email(user_email, subject, body)
    
    @staticmethod
    def send_otp_email(user_email, otp, user_name=None):
        """
        Send OTP verification email
        """
        subject = "Your OTP for Smart Grievance System Verification"
        
        greeting = f"Dear {user_name}," if user_name else "Dear User,"
        
        body = f"""
{greeting}

Thank you for registering with the Smart Grievance System!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 YOUR VERIFICATION CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your One-Time Password (OTP) is:

        {otp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ IMPORTANT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• This OTP is valid for 5 minutes only
• Do not share this OTP with anyone
• If you didn't request this, please ignore this email

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 SECURITY TIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Government officials will NEVER ask for your OTP.
Keep your OTP confidential to protect your account.

---
This is an automated message. Please do not reply.
Smart Grievance System | Digital India Initiative 🇮🇳
        """
        
        return EmailService.send_email(user_email, subject, body)
    
    @staticmethod
    def send_welcome_email(user_email, user_name):
        """
        Send welcome email after registration
        """
        subject = "Welcome to Smart Grievance System 🇮🇳"
        
        body = f"""
Dear {user_name},

Welcome to the Smart Grievance Classification and Resolution Tracking System!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ ACCOUNT ACTIVATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your account has been successfully created and verified.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 WHAT YOU CAN DO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Submit grievances with AI-powered classification
✓ Track complaint status in real-time
✓ Receive updates via email
✓ Communicate with officers via comments
✓ Access in 12 Indian languages

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 GET STARTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Login at: http://localhost:8000/login.html

Thank you for trusting us with your concerns.

Best regards,
Smart Grievance System Team
Digital India Initiative 🇮🇳
        """
        
        return EmailService.send_email(user_email, subject, body)
    
    @staticmethod
    def send_password_reset_confirmation(user_email, user_name):
        """
        Send confirmation email after password reset
        """
        subject = "Password Reset Successful - Smart Grievance System"
        
        body = f"""
Dear {user_name},

Your password has been successfully reset.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PASSWORD CHANGED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your account password was changed on {datetime.utcnow().strftime('%B %d, %Y at %I:%M %p UTC')}.

You can now login with your new password.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 SECURITY NOTICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you did NOT request this password change, please contact us immediately.
Your account security is important to us.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 LOGIN NOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Login at: http://localhost:8000/login.html

---
This is an automated message. Please do not reply.
Smart Grievance System | Digital India Initiative 🇮🇳
        """
        
        return EmailService.send_email(user_email, subject, body)
    
    @staticmethod
    def send_comment_notification(user_email, grievance_id, commenter_name, comment_text):
        """
        Send notification when someone comments on a grievance
        """
        subject = f"New Comment on Grievance #{grievance_id}"
        
        tracking_url = f"http://localhost:8000/track.html?id={grievance_id}"
        
        body = f"""
Dear User,

A new comment has been added to your grievance:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 NEW COMMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complaint ID: #{grievance_id}
From: {commenter_name}

Comment:
{comment_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 VIEW & REPLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{tracking_url}

---
This is an automated message. Please do not reply.
Smart Grievance System | Digital India Initiative
        """
        
        return EmailService.send_email(user_email, subject, body)
    
    @staticmethod
    def send_officer_assignment_notification(officer_email, officer_name, grievance_id, complaint_text, department, user_name, user_phone):
        """
        Send notification to officer when a case is assigned by admin
        """
        subject = f"🚨 New Case Assigned - Grievance #{grievance_id}"
        
        officer_portal_url = f"http://localhost:8000/officer.html"
        
        body = f"""
Dear {officer_name},

A new grievance has been assigned to you by the Admin.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CASE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complaint ID: #{grievance_id}
Department: {department}
Status: Assigned to Department

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 COMPLAINANT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {user_name}
Phone: {user_phone}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 COMPLAINT DESCRIPTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{complaint_text[:300]}{'...' if len(complaint_text) > 300 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please review this case and take necessary action.
You can update the status and add comments from your officer portal.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 OFFICER PORTAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{officer_portal_url}

Thank you for your service.

Best regards,
Admin Team
Smart Grievance System | Digital India Initiative 🇮🇳
        """
        
        return EmailService.send_email(officer_email, subject, body)
    
    @staticmethod
    def send_status_update_notification(user_email, user_name, grievance_id, old_status, new_status, update_message, department, officer_name):
        """
        Send notification to user when officer updates case status
        """
        subject = f"Status Update: Grievance #{grievance_id} - {new_status}"
        
        tracking_url = f"http://localhost:8000/track.html?id={grievance_id}"
        
        # Status emoji mapping
        status_emoji = {
            'Received': '📥',
            'Assigned to Department': '📋',
            'Under Progress': '🔄',
            'Investigation': '🔍',
            'Reviewed': '✅',
            'Resolved': '🎉',
            'Closed': '🔒'
        }
        
        emoji = status_emoji.get(new_status, '📌')
        
        body = f"""
Dear {user_name},

Your grievance status has been updated!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{emoji} STATUS UPDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complaint ID: #{grievance_id}
Department: {department}

Previous Status: {old_status}
Current Status: {new_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👮 OFFICER UPDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Updated by: {officer_name}

Message:
{update_message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 TRACK YOUR COMPLAINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View full timeline and add comments:
{tracking_url}

Thank you for your patience.

Best regards,
Smart Grievance System Team
Digital India Initiative 🇮🇳
        """
        
        return EmailService.send_email(user_email, subject, body)
