from typing import Union
from unittest.mock import patch

from talelio_backend.app_account.use_cases.register_account import register_account, verify_account
from talelio_backend.tests.utils.constants import EMAIL_TALEL, PASSWORD, USERNAME_TALEL
from talelio_backend.tests.utils.mocks import FakeUnitOfWork, generate_verification_token


def account_registration_helper(uow: Union[FakeUnitOfWork, None] = None,
                                email: str = EMAIL_TALEL,
                                username: str = USERNAME_TALEL) -> FakeUnitOfWork:
    with patch('talelio_backend.app_account.domain.account_model.smtplib.SMTP_SSL'):
        if not uow:
            uow = FakeUnitOfWork()

        register_account(uow, email, PASSWORD, username)  # type: ignore

        return uow


def account_verification_helper(uow: FakeUnitOfWork, email: str = EMAIL_TALEL) -> None:
    verification_token = generate_verification_token({'email': email})
    verify_account(uow, verification_token)  # type: ignore
