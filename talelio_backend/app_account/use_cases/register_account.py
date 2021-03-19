from os import getenv

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.auth import generate_password_hash
from talelio_backend.data.uow import UnitOfWork


class AccountRegistrationError(Exception):
    pass


class AccountVerificationError(Exception):
    pass


def register_account(uow: UnitOfWork, email: str, password: str, username: str) -> Account:
    whitelisted_emails = getenv('WHITELISTED_EMAILS')

    if whitelisted_emails is not None and email not in whitelisted_emails.split(','):
        raise AccountRegistrationError('Email not whitelisted')

    with uow:
        if uow.account.get(Account, email=email) is not None:
            raise AccountRegistrationError(f"Account with the email '{email}' already exists")

        password_hash = generate_password_hash(password)
        user = User(username)
        account = Account(email, password_hash, user)

        account_record = uow.account.add(account)
        uow.commit()

        verification_token = account.generate_verification_token
        account.send_registration_email(verification_token)

        return account_record


def verify_account(uow: UnitOfWork, token: str) -> Account:
    registration_details = Account.validate_verification_token(token)
    email = registration_details['email']

    with uow:
        account_record = uow.account.get(Account, email=email)

        if account_record is None:
            raise AccountVerificationError(f"No registered account with the email '{email}'")

        if account_record.verified:
            raise AccountVerificationError('Account already verified')

        setattr(account_record, 'verified', True)
        uow.commit()

        return account_record
