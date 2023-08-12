from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import Authentication
from talelio_backend.identity_and_access.token_store import TokenStore
from talelio_backend.shared.exceptions import AccountError, TokenError
from talelio_backend.shared.utils.time import generate_time_from_now


def generate_access_token(user_id: int, username: str) -> str:
    thirty_mins_from_now = generate_time_from_now(seconds=1800)
    payload = {'user_id': user_id, 'username': username, 'exp': thirty_mins_from_now}

    return Authentication.generate_token(payload)


def get_access_token(uow: UnitOfWork, email: str, password: str) -> str:
    error_msg = 'Invalid username or password'

    with uow:
        account_record = uow.account.get_by_email(email)

        if account_record is None:
            raise AccountError(error_msg)

        password_hash = account_record[4]
        user_id = account_record[6]
        username = account_record[7]

        if not Authentication().check_password_hash(password, password_hash):
            raise AccountError(error_msg)

        access_token = generate_access_token(user_id, username)

        return access_token


def set_refresh_token(token_store: TokenStore, user_id: int, username: str) -> str:
    now = generate_time_from_now(seconds=0)

    payload = {'user_id': user_id, 'username': username, 'iat': now}
    refresh_token = Authentication.generate_token(payload)

    token_store.set_token(user_id, refresh_token)

    return refresh_token


def verify_refresh_token(token_store: TokenStore, user_id: int, refresh_token: str) -> bool:
    stored_refresh_token = token_store.get_token(user_id)

    if not stored_refresh_token:
        raise TokenError('No stored refresh token for user')

    if not stored_refresh_token == refresh_token:
        raise TokenError('Provided refresh token not matching stored refresh token')

    return True


def delete_refresh_token(token_store: TokenStore, user_id: int) -> bool:
    if token_store.delete_token(user_id) == 0:
        raise TokenError('No token to delete')

    return True
