import smtplib
from email.message import EmailMessage
from os import getenv
from typing import Dict, cast

from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer

SECRET_KEY = cast(str, getenv('SECRET_KEY'))
EMAIL_USER = cast(str, getenv('EMAIL_USER'))
EMAIL_PASS = cast(str, getenv('EMAIL_PASS'))
EMAIL_SENDER = cast(str, getenv('EMAIL_SENDER'))
EMAIL_SERVER = cast(str, getenv('EMAIL_SERVER'))


class Account:
    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    @property
    def generate_verification_token(self) -> str:
        expire_sec = 900
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, expire_sec)
        token = serializer.dumps({'email': self.email, 'password': self.password}).decode('utf-8')

        return token

    @staticmethod
    def validate_registration_token(token: str) -> Dict[str, str]:
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY)

        try:
            serialized_token = serializer.loads(token)
            return serialized_token
        except SignatureExpired as error:
            raise SignatureExpired('Invalid registration token') from error

    def _compose_email_message(self, subject: str, content: str) -> EmailMessage:
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = EMAIL_SENDER
        message['To'] = self.email
        message.set_content(content)

        return message

    def send_registration_email(self, token: str) -> None:
        subject = 'Test registration email'
        content = f'http://localhost:5000/v1/account/register/{token}'
        message = self._compose_email_message(subject, content)

        with smtplib.SMTP_SSL(EMAIL_SERVER, 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(message)
