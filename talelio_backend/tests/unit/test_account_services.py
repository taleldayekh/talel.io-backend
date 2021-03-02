from os import environ
from time import sleep
from unittest.mock import patch

import pytest
from itsdangerous import SignatureExpired

from talelio_backend.app_account.use_cases.register_account import (AccountRegistrationError,
                                                                    register_account)
from talelio_backend.tests.utils.constants import EMAIL, PASSWORD
from talelio_backend.tests.utils.mocks import FakeUnitOfWork, generate_verification_token

account_registration_data = {'email': EMAIL, 'password': PASSWORD}


def test_can_register_account() -> None:
    token = generate_verification_token(None, account_registration_data)
    uow = FakeUnitOfWork()

    register_account(uow, token)  # type: ignore
    account = list(uow.account.fake_db)[0]

    assert uow.committed
    assert account.email == EMAIL
    assert account.password == PASSWORD


def test_cannot_register_account_with_expired_registration_token() -> None:
    token = generate_verification_token(0, account_registration_data)

    # TODO: Replace sleep with mocked token expiration or a library like FreezeGun
    sleep(1)
    uow = FakeUnitOfWork()

    with pytest.raises(SignatureExpired, match='Invalid registration token'):
        register_account(uow, token)  # type: ignore


@patch.dict(environ, {'WHITELISTED_EMAILS': ''})
def test_cannot_register_account_with_non_whitelisted_email() -> None:
    token = generate_verification_token(None, account_registration_data)
    uow = FakeUnitOfWork()

    with pytest.raises(AccountRegistrationError, match='Email not whitelisted'):
        register_account(uow, token)  # type: ignore
