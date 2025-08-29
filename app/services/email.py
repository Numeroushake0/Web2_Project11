from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_user,
    MAIL_PASSWORD=settings.smtp_password,
    MAIL_FROM=settings.smtp_user,
    MAIL_PORT=settings.smtp_port,
    MAIL_SERVER=settings.smtp_host,
    MAIL_FROM_NAME="Contacts API",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_email(email: EmailStr, subject: str, body: str):
    """
    Send an email with HTML content.

    Args:
        email (EmailStr): Recipient email address.
        subject (str): Subject of the email.
        body (str): HTML body content of the email.
    """
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
