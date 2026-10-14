import os
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def send_email(
    recipient_email: str,
    subject: str,
    body: str
):
    """
    Send normal email.
    """

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email

    msg.set_content(body)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )

        smtp.send_message(msg)

    return True


def send_email_with_attachment(
    recipient_email: str,
    subject: str,
    body: str,
    attachment_path: str
):
    """
    Send email with PDF attachment.
    """

    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email

    msg.set_content(body)

    with open(
        attachment_path,
        "rb"
    ) as file:

        file_data = file.read()

        file_name = os.path.basename(
            attachment_path
        )

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename=file_name
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )

        smtp.send_message(msg)

    return True


if __name__ == "__main__":

    send_email(
        recipient_email="yourtestmail@gmail.com",
        subject="Iyarkural Email Service Test",
        body="Email service is working successfully."
    )

    print("✅ Test Email Sent")