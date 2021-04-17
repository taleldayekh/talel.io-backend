from os import environ
from unittest.mock import patch

import pytest

from talelio_backend.app_account.use_cases.register_account import (AccountError,
                                                                    AccountRegistrationError,
                                                                    AccountVerificationError)
from talelio_backend.tests.integration.helpers import (account_registration_helper,
                                                       account_verification_helper)
from talelio_backend.tests.utils.constants import EMAIL_TALEL, USERNAME_TALEL
from talelio_backend.tests.utils.mocks import FakeUnitOfWork


def test_can_register_account() -> None:
    uow = account_registration_helper()
    account_record = list(uow.account.fake_db)[0]

    assert uow.committed
    assert account_record.email == EMAIL_TALEL
    assert account_record.user.username == USERNAME_TALEL


@patch.dict(environ, {'WHITELISTED_EMAILS': ''})
def test_cannot_register_account_with_non_whitelisted_email() -> None:
    with pytest.raises(AccountRegistrationError, match='Email not whitelisted'):
        account_registration_helper()


def test_cannot_register_account_with_already_registered_email() -> None:
    uow = account_registration_helper()

    with pytest.raises(AccountRegistrationError,
                       match=f"Account with the email '{EMAIL_TALEL}' already exists"):
        account_registration_helper(uow)


def test_can_verify_account() -> None:
    uow = account_registration_helper()
    account_record = list(uow.account.fake_db)[0]

    assert not account_record.verified

    account_verification_helper(uow)

    assert account_record.verified


def test_cannot_verify_non_registered_account() -> None:
    uow = FakeUnitOfWork()

    with pytest.raises(AccountError,
                       match=f"No registered account with the email '{EMAIL_TALEL}'"):
        account_verification_helper(uow)


def test_cannot_verify_already_verified_account() -> None:
    uow = account_registration_helper()
    account_verification_helper(uow)

    with pytest.raises(AccountVerificationError, match='Account already verified'):
        account_verification_helper(uow)
