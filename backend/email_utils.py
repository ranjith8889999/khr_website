"""
Email helper functions using Python stdlib smtplib.
All public functions are async – they offload the blocking SMTP call to a
thread via asyncio.to_thread (Python 3.9+, available in our Python 3.11 image).
"""

import asyncio
import smtplib
import os
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ── Low-level SMTP sender ─────────────────────────────────────────────

def _send_smtp(to_email: str, subject: str, html_body: str) -> None:
    """Blocking SMTP send – call via asyncio.to_thread to avoid blocking event loop."""
    server_host = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    server_port = int(os.getenv('MAIL_PORT', 587))
    username = os.getenv('MAIL_USERNAME', '')
    password = os.getenv('MAIL_PASSWORD', '')
    sender = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@kolanhanmanthreddy.com')
    use_tls = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    use_ssl = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    msg.attach(MIMEText(html_body, 'html'))

    smtp_cls = smtplib.SMTP_SSL if use_ssl else smtplib.SMTP
    with smtp_cls(server_host, server_port) as server:
        if use_tls and not use_ssl:
            server.starttls()
        if username and password:
            server.login(username, password)
        server.sendmail(sender, to_email, msg.as_string())


async def _send(to_email: str, subject: str, html: str) -> None:
    await asyncio.to_thread(_send_smtp, to_email, subject, html)


# ── Confirmation emails ───────────────────────────────────────────────

async def send_complaint_confirmation_email(data: dict) -> None:
    try:
        html = f"""
        <html><body style="font-family:Arial,sans-serif;color:#333;">
            <h2 style="color:#ff9500;">Complaint Acknowledgment</h2>
            <p>Dear {data['name']},</p>
            <p>We have received your complaint and it has been registered in our system.</p>
            <p><strong>Reference Number: {data['reference_number']}</strong></p>
            <p><strong>Category: {data['category']}</strong></p>
            <p><strong>Subject: {data['subject']}</strong></p>
            <p>Your complaint will be reviewed and addressed within 7 working days.</p>
            <p>You can track the status using your reference number.</p>
            <p>Thank you for bringing this to our attention.</p>
            <p style="margin-top:30px;color:#666;">
                Best regards,<br>Kolan Hanmanth Reddy<br>Senior Congress Leader, Quthbullapur
            </p>
        </body></html>"""
        await _send(data['email'], f"Complaint Received - Reference: {data['reference_number']}", html)
        print(f"✓ Complaint email sent to {data['email']} (Ref: {data['reference_number']})")
    except Exception as e:
        print(f"✗ Complaint email error for {data.get('email')}: {e}")
        print(traceback.format_exc())


async def send_feedback_confirmation_email(data: dict) -> None:
    try:
        html = f"""
        <html><body style="font-family:Arial,sans-serif;color:#333;">
            <h2 style="color:#ff9500;">Thank You for Your Feedback</h2>
            <p>Dear {data['name']},</p>
            <p>We have received your feedback and appreciate your input.</p>
            <p><strong>Category: {data['category']}</strong></p>
            <p><strong>Rating: {data['rating']}/5</strong></p>
            <p>Your feedback helps us improve our services and better serve the community.</p>
            <p style="margin-top:30px;color:#666;">
                Best regards,<br>Kolan Hanmanth Reddy<br>Senior Congress Leader, Quthbullapur
            </p>
        </body></html>"""
        await _send(data['email'], 'We Value Your Feedback', html)
        print(f"✓ Feedback email sent to {data['email']}")
    except Exception as e:
        print(f"✗ Feedback email error for {data.get('email')}: {e}")
        print(traceback.format_exc())


async def send_skills_confirmation_email(data: dict) -> None:
    try:
        html = f"""
        <html><body style="font-family:Arial,sans-serif;color:#333;">
            <h2 style="color:#ff9500;">Skills Development Program Registration</h2>
            <p>Dear {data['name']},</p>
            <p>Your registration for the Skills Development Program has been received.</p>
            <p><strong>Education Level: {data['education']}</strong></p>
            <p><strong>Location: {data['location']}</strong></p>
            <p>Your application is currently under review. You will receive further updates shortly.</p>
            <p style="margin-top:30px;color:#666;">
                Best regards,<br>Kolan Hanmanth Reddy<br>Senior Congress Leader, Quthbullapur
            </p>
        </body></html>"""
        await _send(data['email'], 'Registration Confirmed - Skills Development Program', html)
        print(f"✓ Skills email sent to {data['email']}")
    except Exception as e:
        print(f"✗ Skills email error for {data.get('email')}: {e}")
        print(traceback.format_exc())


async def send_contact_confirmation_email(data: dict) -> None:
    try:
        html = f"""
        <html><body style="font-family:Arial,sans-serif;color:#333;">
            <h2 style="color:#ff9500;">Message Acknowledgment</h2>
            <p>Dear {data['name']},</p>
            <p>We have received your message and will get back to you soon.</p>
            <p><strong>Subject: {data['subject']}</strong></p>
            <p>Thank you for reaching out to us.</p>
            <p style="margin-top:30px;color:#666;">
                Best regards,<br>Kolan Hanmanth Reddy<br>Senior Congress Leader, Quthbullapur
            </p>
        </body></html>"""
        await _send(data['email'], 'Message Received', html)
        print(f"✓ Contact email sent to {data['email']}")
    except Exception as e:
        print(f"✗ Contact email error for {data.get('email')}: {e}")
        print(traceback.format_exc())


async def send_test_email(recipient: str) -> None:
    """Used by the /api/test-email endpoint. Raises on failure so caller gets error details."""
    html = """
    <html><body style="font-family:Arial,sans-serif;color:#333;">
        <h2 style="color:#ff9500;">Email Configuration Test</h2>
        <p>This is a test email from the Kolan Hanmanth Reddy website.</p>
        <p>If you receive this email, your SMTP configuration is working correctly!</p>
        <p style="margin-top:30px;color:#666;">Best regards,<br>KHR Website</p>
    </body></html>"""
    await _send(recipient, 'Test Email - KHR Website', html)
