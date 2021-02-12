import smtplib
from email.message import EmailMessage
from os import getenv
from typing import cast

from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer


class Account:
    secret_key = cast(str, getenv('SECRET_KEY'))
    email_user = cast(str, getenv('EMAIL_USER'))
    email_pass = cast(str, getenv('EMAIL_PASS'))
    email_sender = cast(str, getenv('EMAIL_SENDER'))
    email_server = cast(str, getenv('EMAIL_SERVER'))

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    @property
    def generate_verification_token(self) -> str:
        expire_sec = 900
        serializer = TimedJSONWebSignatureSerializer(self.secret_key, expire_sec)
        token = serializer.dumps({'email': self.email, 'password': self.password}).decode('utf-8')

        return token

    def validate_verification_token(self, token: str) -> bool:
        serializer = TimedJSONWebSignatureSerializer(self.secret_key)

        try:
            serializer.loads(token)
        except SignatureExpired:
            return False
        return True

    def _compose_email_message(self, subject: str, content: str) -> EmailMessage:
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = self.email_sender
        message['To'] = self.email
        message.set_content(content)

        return message

    def send_registration_email(self, verification_token: str) -> None:
        subject = 'Test registration email'
        content = f'http://localhost:5000/account/register/{verification_token}'
        message = self._compose_email_message(subject, content)

        with smtplib.SMTP_SSL(self.email_server, 465) as smtp:
            smtp.login(self.email_user, self.email_pass)
            smtp.send_message(message)
