import smtplib
from email.message import EmailMessage
from os import getenv
from typing import Dict, cast

from itsdangerous import BadSignature, TimedJSONWebSignatureSerializer

from talelio_backend.app_user.domain.user_model import User

ENV = getenv('ENV')
SECRET_KEY = cast(str, getenv('SECRET_KEY'))
EMAIL_USER = cast(str, getenv('EMAIL_USER'))
EMAIL_PASS = cast(str, getenv('EMAIL_PASS'))
EMAIL_SENDER = cast(str, getenv('EMAIL_SENDER'))
EMAIL_SERVER = cast(str, getenv('EMAIL_SERVER'))

PROD_VERIFICATION_URL = 'https://api.talel.io/v1/account/verify'
DEV_VERIFICATION_URL = 'http://localhost:5000/v1/account/verify'


class Account:
    def __init__(self, email: str, password: str, user: User, verified: bool = False) -> None:
        self.email = email
        self.password = password
        self.user = user
        self.verified = verified

    @property
    def generate_verification_token(self) -> str:
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY)
        token = serializer.dumps({'email': self.email}).decode('utf-8')

        return token

    @staticmethod
    def validate_verification_token(token: str) -> Dict[str, str]:
        serializer = TimedJSONWebSignatureSerializer(SECRET_KEY)

        try:
            serialized_token = serializer.loads(token)
            return serialized_token
        except BadSignature as error:
            raise BadSignature('Invalid verification token') from error

    def _compose_email_message(self, subject: str, content: str) -> EmailMessage:
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = EMAIL_SENDER
        message['To'] = self.email
        message.set_content(content)

        return message

    def send_registration_email(self, token: str) -> None:
        subject = 'Test registration email'
        content = (f'{PROD_VERIFICATION_URL}/{token}'
                   if ENV == 'production' else f'{DEV_VERIFICATION_URL}/{token}')
        message = self._compose_email_message(subject, content)

        with smtplib.SMTP_SSL(EMAIL_SERVER, 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(message)
