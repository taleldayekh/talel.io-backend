from os import getenv

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import (AccountError, AccountRegistrationError,
                                             AccountVerificationError)
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import Authentication


def register_account(uow: UnitOfWork, email: str, password: str, username: str) -> Account:
    with uow:
        password_hash = Authentication().generate_password_hash(password)

        user = User(username)
        account = Account(email, password_hash)

        uow.account.create(account, user)

        return {}

    # whitelisted_emails = getenv('WHITELISTED_EMAILS')

    # if whitelisted_emails is not None and email not in whitelisted_emails.split(','):
    #     raise AccountRegistrationError('Email not whitelisted')

    # with uow:
    #     # if uow.account.get(Account, email=email) is not None:
    #     #     raise AccountRegistrationError(f"Account with the email '{email}' already exists")

    #     # if uow.user.get(User, username=username):
    #     #     raise AccountRegistrationError(
    #     #         f"Account with the username '{username}' already exists")

    #     password_hash = Authentication().generate_password_hash(password)
    #     # user = User(username)
    #     account = Account(email, password_hash)

    #     uow.account.create(account)

    #     # account_record = uow.account.add(account)
    #     # uow.commit()

    #     account_record = uow.account.get(Account, email=email)
    #     verification_token = account.generate_verification_token
    #     account.send_registration_email(verification_token)

    #     # return account_record
    #     return {}


def verify_account(uow: UnitOfWork, token: str) -> Account:
    registration_details = Account.validate_verification_token(token)
    email = registration_details['email']

    with uow:
        account_record = uow.account.get(Account, email=email)

        if account_record is None:
            raise AccountError(f"No registered account with the email '{email}'")

        if account_record.verified:
            raise AccountVerificationError('Account already verified')

        setattr(account_record, 'verified', True)
        uow.commit()

        account_record = uow.account.get(Account, email=email)

        return account_record
