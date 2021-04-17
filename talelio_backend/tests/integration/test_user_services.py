import pytest

from talelio_backend.app_user.use_cases.authenticate_user import get_access_token
from talelio_backend.core.exceptions import AccountError
from talelio_backend.tests.integration.helpers import account_registration_helper
from talelio_backend.tests.utils.constants import EMAIL_BIANCA, EMAIL_TALEL, PASSWORD


def test_can_get_access_token_for_user() -> None:
    uow = account_registration_helper()
    access_token = get_access_token(uow, EMAIL_TALEL, PASSWORD)  # type: ignore

    assert access_token['access_token']


def test_cannot_get_access_token_for_non_registered_user() -> None:
    uow = account_registration_helper()

    with pytest.raises(AccountError, match='Invalid username or password'):
        get_access_token(uow, EMAIL_BIANCA, PASSWORD)  # type: ignore


def test_cannot_get_access_token_with_invalid_password() -> None:
    uow = account_registration_helper()

    with pytest.raises(AccountError, match='Invalid username or password'):
        get_access_token(uow, EMAIL_TALEL, '')  # type: ignore
