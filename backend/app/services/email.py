import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


async def send_notification(name: str, phone: str, email: str, message: str):
    if not settings.smtp_user or not settings.smtp_password:
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"New Contact — {name}"
    msg["From"] = settings.smtp_user
    msg["To"] = settings.notification_email

    html = f"""
    <h2>New Contact Form Submission</h2>
    <table style="border-collapse:collapse;width:100%;max-width:500px;">
      <tr><td style="padding:8px;font-weight:bold;">Name</td><td style="padding:8px;">{name}</td></tr>
      <tr><td style="padding:8px;font-weight:bold;">Phone</td><td style="padding:8px;">{phone}</td></tr>
      <tr><td style="padding:8px;font-weight:bold;">Email</td><td style="padding:8px;">{email}</td></tr>
      <tr><td style="padding:8px;font-weight:bold;">Message</td><td style="padding:8px;">{message}</td></tr>
    </table>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.smtp_user, settings.notification_email, msg.as_string())
    except Exception as e:
        print(f"Email send failed: {e}")
