import pytest
from freezegun import freeze_time
from jwt.exceptions import ExpiredSignatureError

from talelio_backend.app_user.use_cases.authenticate_user import (delete_refresh_token,
                                                                  set_refresh_token,
                                                                  verify_refresh_token)
from talelio_backend.core.exceptions import AccountError, TokenError
from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.shared.utils import generate_time_from_now
from talelio_backend.tests.constants import FAKE_TOKEN, INITIAL_USER_ID, USERNAME_TALEL
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


def test_can_verify_refresh_token() -> None:
    token_store = FakeTokenStore()
    verified_refresh_token = verify_refresh_token(
        token_store,  # type: ignore
        INITIAL_USER_ID,
        FAKE_TOKEN)

    assert verified_refresh_token


def test_cannot_verify_refresh_token_for_non_existing_user_id() -> None:
    token_store = FakeTokenStore()
    invalid_user_id = INITIAL_USER_ID + 1986

    with pytest.raises(TokenError, match='No stored refresh token for user'):
        verify_refresh_token(token_store, invalid_user_id, FAKE_TOKEN)  # type: ignore


def test_cannot_verify_non_existing_refresh_token() -> None:
    token_store = FakeTokenStore()
    invalid_refresh_token = 'invalid.refresh.token'

    with pytest.raises(TokenError,
                       match='Provided refresh token not matching stored refresh token'):
        verify_refresh_token(token_store, INITIAL_USER_ID, invalid_refresh_token)  # type: ignore


def test_can_delete_refresh_token() -> None:
    token_store = FakeTokenStore()
    deleted_refresh_token = delete_refresh_token(token_store, INITIAL_USER_ID)  # type: ignore

    assert deleted_refresh_token


def test_cannot_delete_refresh_token_for_non_existing_user_id() -> None:
    token_store = FakeTokenStore()
    invalid_user_id = INITIAL_USER_ID + 1986

    with pytest.raises(TokenError, match='No token to delete'):
        delete_refresh_token(token_store, invalid_user_id)  # type: ignore
