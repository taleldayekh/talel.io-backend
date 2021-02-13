from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.core.db import session_manager


def send_registration_email(email: str, password: str) -> None:
    account = Account(email, password)
    verification_token = account.generate_verification_token
    account.send_registration_email(verification_token)


def register_account(token: str) -> None:
    registration_details = Account.validate_registration_token(token)
    email = registration_details['email']
    password = registration_details['password']

    with session_manager() as session:
        session.add(Account(email, password))
        session.commit()
