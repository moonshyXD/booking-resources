from email.message import EmailMessage
import aiosmtplib

class EmailSender:
    def __init__(self, smtp_config):
        self.from_address = smtp_config.from_address
        self.smtp_server = smtp_config.server
        self.port = smtp_config.port
        self.username = smtp_config.username
        self.password = smtp_config.password
        self.subject = smtp_config.subject

    async def send_email(self, email: str, message: str):
        email_message = EmailMessage()

        email_message["From"] = self.from_address
        email_message["To"] = email
        email_message["Subject"] = self.subject

        email_message.set_content(message, subtype="html")

        await aiosmtplib.send(
            email_message,
            hostname=self.smtp_server,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=True
        )