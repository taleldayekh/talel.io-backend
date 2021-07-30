import pytest
from freezegun import freeze_time
from jwt.exceptions import ExpiredSignatureError

from talelio_backend.app_user.use_cases.authenticate_user import set_refresh_token
from talelio_backend.core.exceptions import AccountError
from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.shared.utils import generate_time_from_now
from talelio_backend.tests.constants import INITIAL_USER_ID, USERNAME_TALEL
from talelio_backend.tests.integration.helpers import (get_access_token_helper,
                                                       register_account_helper)
from talelio_backend.tests.mocks.data import FakeTokenStore, FakeUnitOfWork


def test_can_get_access_token_for_user() -> None:
    uow = register_account_helper()
    access_token = get_access_token_helper(uow)

    username = Authentication().get_jwt_identity(access_token)['username']

    assert username == USERNAME_TALEL


def test_access_token_expires_after_30_min() -> None:
    thirtyone_mins_from_now = generate_time_from_now(1860)
    uow = register_account_helper()
    access_token = get_access_token_helper(uow)

    with freeze_time(thirtyone_mins_from_now):
        with pytest.raises(ExpiredSignatureError):
            Authentication.verify_token(access_token)


def test_cannot_get_access_token_for_non_registered_user() -> None:
    uow = FakeUnitOfWork()

    with pytest.raises(AccountError, match='Invalid username or password'):
        get_access_token_helper(uow)


def test_cannot_get_access_token_with_invalid_password() -> None:
    uow = register_account_helper()

    with pytest.raises(AccountError, match='Invalid username or password'):
        get_access_token_helper(uow, password='')


def test_can_set_refresh_token_for_user() -> None:
    token_store = FakeTokenStore()
    refresh_token = set_refresh_token(token_store, INITIAL_USER_ID, USERNAME_TALEL)  # type: ignore

    user_id, username, iat = Authentication().get_jwt_identity(refresh_token).values()

    assert username == USERNAME_TALEL
    assert user_id == INITIAL_USER_ID
    assert iat
