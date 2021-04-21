from os import environ
from unittest.mock import patch

import pytest

from talelio_backend.app_account.use_cases.register_account import (AccountError,
                                                                    AccountRegistrationError,
                                                                    AccountVerificationError)
from talelio_backend.tests.integration.helpers import (register_account_helper,
                                                       verify_account_helper)
from talelio_backend.tests.mocks.data import FakeUnitOfWork
from talelio_backend.tests.utils.constants import EMAIL_BIANCA, EMAIL_TALEL, USERNAME_TALEL


def test_can_register_account() -> None:
    uow = register_account_helper()
    account_record = uow.fake_db['account'][0]

    assert uow.committed
    assert account_record.email == EMAIL_TALEL
    assert account_record.user.username == USERNAME_TALEL


@patch.dict(environ, {'WHITELISTED_EMAILS': ''})
def test_cannot_register_account_with_non_whitelisted_email() -> None:
    with pytest.raises(AccountRegistrationError, match='Email not whitelisted'):
        register_account_helper()


def test_cannot_register_account_with_already_registered_email() -> None:
    uow = register_account_helper()

    with pytest.raises(AccountRegistrationError,
                       match=f"Account with the email '{EMAIL_TALEL}' already exists"):
        register_account_helper(uow)


def test_cannot_register_account_with_already_registered_username() -> None:
    uow = register_account_helper()

    with pytest.raises(AccountRegistrationError,
                       match=f"Account with the username '{USERNAME_TALEL}' already exists"):
        register_account_helper(uow, EMAIL_BIANCA, USERNAME_TALEL)


def test_can_verify_account() -> None:
    uow = register_account_helper()
    account_record = uow.fake_db['account'][0]

    assert not account_record.verified

    verify_account_helper(uow)

    assert account_record.verified


def test_cannot_verify_non_registered_account() -> None:
    uow = FakeUnitOfWork()

    with pytest.raises(AccountError,
                       match=f"No registered account with the email '{EMAIL_TALEL}'"):
        verify_account_helper(uow)


def test_cannot_verify_already_verified_account() -> None:
    uow = register_account_helper()
    verify_account_helper(uow)

    with pytest.raises(AccountVerificationError, match='Account already verified'):
        verify_account_helper(uow)
