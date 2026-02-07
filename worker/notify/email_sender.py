import os
from email.message import EmailMessage
import smtplib

def send_email(to_email: str, subject: str, body: str):

   # Load credentials from environment variables
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise Exception("Missing SMTP_EMAIL or SMTP_PASSWORD in environment")
    
    # Gmail SMTP server
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587

    # Build the email message
    msg = EmailMessage()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    #send email
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

    # print(f"Email sent to {RECEIVER_email}")


