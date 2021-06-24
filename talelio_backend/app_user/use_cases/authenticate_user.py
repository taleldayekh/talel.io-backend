from typing import Dict

from talelio_backend.app_account.domain.account_model import Account
from talelio_backend.core.exceptions import AccountError
from talelio_backend.data.uow import UnitOfWork
from talelio_backend.identity_and_access.authentication import JWT, check_password_hash
from talelio_backend.shared.utils import generate_time_from_now


def get_access_token(uow: UnitOfWork, email: str, password: str) -> Dict[str, str]:
    error_msg = 'Invalid username or password'

    with uow:
        account_record = uow.account.get(Account, email=email)

        if account_record is None:
            raise AccountError(error_msg)

        password_hash = account_record.password

        if not check_password_hash(password, password_hash):
            raise AccountError(error_msg)

        thirty_mins_from_now = generate_time_from_now(seconds=1800)

        payload = {
            'user_id': account_record.user.id,
            'username': account_record.user.username,
            'exp': thirty_mins_from_now
        }
        access_token = JWT.generate_token(payload)

        return {'access_token': access_token}
