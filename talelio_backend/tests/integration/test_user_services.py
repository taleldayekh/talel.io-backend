import pytest

from talelio_backend.core.exceptions import AccountError
from talelio_backend.tests.integration.helpers import (get_access_token_helper,
                                                       register_account_helper)
from talelio_backend.tests.mocks.data import FakeUnitOfWork


def test_can_get_access_token_for_user() -> None:
    uow = register_account_helper()
    access_token = get_access_token_helper(uow)

    assert access_token['access_token']


def test_cannot_get_access_token_for_non_registered_user() -> None:
    uow = FakeUnitOfWork()

    with pytest.raises(AccountError, match='Invalid username or password'):
        get_access_token_helper(uow)


def test_cannot_get_access_token_with_invalid_password() -> None:
    uow = register_account_helper()

    with pytest.raises(AccountError, match='Invalid username or password'):
        get_access_token_helper(uow, password='')
