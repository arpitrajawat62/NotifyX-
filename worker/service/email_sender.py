import os
from email.message import EmailMessage
import smtplib


def send_email(to_email: str, subject: str, body: str):

    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    if not SMTP_EMAIL or not SMTP_PASSWORD:
        raise Exception("Missing SMTP_EMAIL or SMTP_PASSWORD")

    msg = EmailMessage()
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)