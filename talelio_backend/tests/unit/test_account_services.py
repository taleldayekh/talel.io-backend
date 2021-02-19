from os import getenv
from time import sleep
from typing import cast

import pytest
from itsdangerous import SignatureExpired, TimedJSONWebSignatureSerializer

from talelio_backend.app_account.use_cases.register_account import register_account
from talelio_backend.tests.utils.mocks import FakeUnitOfWork

SECRET_KEY = cast(str, getenv('SECRET_KEY'))
EMAIL = 'talel@talel.talel'
PASSWORD = 'password'


def test_can_register_account() -> None:
    serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, None)
    token = serializer.dumps({'email': EMAIL, 'password': PASSWORD})
    uow = FakeUnitOfWork()

    register_account(uow, str(token, 'utf-8'))  # type: ignore
    account = list(uow.account.fake_db)[0]

    assert uow.committed
    assert account.email == EMAIL
    assert account.password == PASSWORD


def test_cannot_register_account_with_expired_registration_token() -> None:
    serializer = TimedJSONWebSignatureSerializer(SECRET_KEY, 0)
    token = serializer.dumps({'email': EMAIL, 'password': PASSWORD})

    # TODO: Replace sleep with mocked token expiration or a library like FreezeGun
    sleep(1)
    uow = FakeUnitOfWork()

    with pytest.raises(SignatureExpired, match='Invalid registration token'):
        register_account(uow, str(token, 'utf-8'))  # type: ignore
