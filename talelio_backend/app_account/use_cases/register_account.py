from os import getenv

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.data.uow import UnitOfWork


class AccountRegistrationError(Exception):
    pass


def send_registration_email(email: str, password: str) -> None:
    account = Account(email, password)
    verification_token = account.generate_verification_token
    account.send_registration_email(verification_token)


def register_account(uow: UnitOfWork, token: str) -> None:
    registration_details = Account.validate_registration_token(token)
    email = registration_details['email']
    password = registration_details['password']
    whitelisted_emails = getenv('WHITELISTED_EMAILS')

    if whitelisted_emails is not None and email not in whitelisted_emails.split(','):
        raise AccountRegistrationError('Email not whitelisted')

    with uow:
        uow.account.add(Account(email, password))
        uow.commit()
