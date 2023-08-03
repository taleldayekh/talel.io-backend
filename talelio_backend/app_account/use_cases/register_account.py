from os import getenv

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.app_user.domain.user_model import User
from talelio_backend.core.exceptions import (AccountError, AccountRegistrationError,
                                             AccountVerificationError)
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import Authentication


def register_account(uow: UnitOfWork, email: str, password: str, username: str) -> Account:
    whitelisted_emails = getenv('WHITELISTED_EMAILS')

    if whitelisted_emails is not None and email not in whitelisted_emails.split(','):
        raise AccountRegistrationError('Email not whitelisted')

    with uow:
        if uow.account.get_by_email(email) is not None:
            raise AccountRegistrationError(f"Account with the email '{email}' already exists")

        if len(uow.user.get_by_username(username)):
            raise AccountRegistrationError(
                f"Account with the username '{username}' already exists")

        password_hash = Authentication().generate_password_hash(password)

        user = User(username)
        account = Account(email, password_hash)

        account_id = uow.account.create(account, user)
        account_record = uow.account.get_by_id(account_id)

        verification_token = account.generate_verification_token
        account.send_registration_email(verification_token)

        return {
            "id": account_record[0],
            "created_at": account_record[1],
            "updated_at": account_record[2],
            "email": account_record[3],
            "verified": account_record[5],
            "user": {
                "id": account_record[6],
                "username": account_record[7],
                "location": account_record[8],
                "avatar_url": account_record[9]
            }
        }


# TODO: Refactor to use SQL
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
