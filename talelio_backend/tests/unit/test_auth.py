from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.tests.constants import PASSWORD

SALT = 'talel'

auth = Authentication()


def test_can_generate_password_hash_with_new_salt() -> None:
    password_hash = auth.generate_password_hash(PASSWORD)
    salt = password_hash.split(',')[1]

    assert len(salt) == 5
    assert salt.isascii()


def test_can_generate_password_hash_when_provided_salt() -> None:
    password_hash = auth.generate_password_hash(PASSWORD, SALT)
    salt = password_hash.split(',')[1]

    assert salt == SALT


def test_valid_password_returns_true_when_checking_hash() -> None:
    password_hash = auth.generate_password_hash(PASSWORD)
    password = auth.check_password_hash(PASSWORD, password_hash)

    assert password


def test_invalid_password_returns_false_when_checking_hash() -> None:
    password_hash = auth.generate_password_hash(PASSWORD)
    password = auth.check_password_hash('invalid password', password_hash)

    assert not password
