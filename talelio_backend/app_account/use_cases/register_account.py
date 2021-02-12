from talelio_backend.app_account.domain.account_model import Account


def send_registration_email(email: str, password: str) -> None:
    account = Account(email, password)
    verification_token = account.generate_verification_token
    account.send_registration_email(verification_token)


def register_account() -> None:
    pass
