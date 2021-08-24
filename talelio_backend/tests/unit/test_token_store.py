from fakeredis import FakeStrictRedis

from talelio_backend.identity_and_access.token_store import TokenStore
from talelio_backend.tests.constants import FAKE_TOKEN


def fake_token_store() -> TokenStore:
    return TokenStore(redis=FakeStrictRedis())


def test_can_set_and_get_token() -> None:
    token_store = fake_token_store()
    token_store.set_token(1, FAKE_TOKEN)

    assert token_store.get_token(1) == FAKE_TOKEN


def test_cannot_get_token_for_non_existing_user_id() -> None:
    token_store = fake_token_store()
    token = token_store.get_token(1)

    assert token is None


def test_deleting_token_for_existing_user_id_returns_exit_code_1() -> None:
    token_store = fake_token_store()
    token_store.set_token(1, FAKE_TOKEN)

    assert token_store.get_token(1) == FAKE_TOKEN

    deleted_token = token_store.delete_token(1)

    assert deleted_token == 1


def test_deleting_token_for_non_existing_user_id_returns_exit_code_0() -> None:
    token_store = fake_token_store()
    deleted_token = token_store.delete_token(1)

    assert deleted_token == 0
